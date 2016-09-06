from server import app, get_language_count
from flask import session
import unittest
from model import db, connect_to_db, Course, example_data
from helpers import get_user_by_email, get_user_by_session, is_favorited, is_taken, is_enrolled

class FlaskTests(unittest.TestCase):

	def setUp(self):
		"""Set up by creating fake client."""

		self.client = app.test_client()
		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'

	def test_index(self):
		"""Test for main search page."""

		# client = app.test_client()
		result = self.client.get("/")
		self.assertEqual(result.status_code, 200)
		self.assertIn("<h1>What do you want to learn about?</h1>", result.data)


	def test_register_form(self):
		"""Test for registration page."""

		# client = app.test_client()
		result = self.client.get("/register")
		self.assertEqual(result.status_code, 200)
		self.assertIn("Sign up now", result.data)


	def test_login_form(self):
		"""Test for registration page."""

		# client = app.test_client()
		result = self.client.get("/login")
		self.assertEqual(result.status_code, 200)
		self.assertIn("Please log in", result.data)


	def test_bookmark(self):
		"""Test adding a course to enrolled."""

		result = self.client.post("/bookmark", 
								data={"current_user": None,
								"id": 2}, follow_redirects=True)

		self.assertIn("You must be signed in", result.data)



class FlaskDBTests(unittest.TestCase):
	"""Tests querying and changing database."""

	def setUp(self):
		"""Set up by creating testdb and fake client."""

		self.client = app.test_client()
		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		connect_to_db(app, "postgresql:///testdb")

		with self.client as c:
			with c.session_transaction() as session:
				session['current_user'] = "jane@email.com"

		db.create_all()
		example_data()

	def tearDown(self):
		"""Tear down by droping testdb."""

		db.session.close()
		db.drop_all()


	def test_login(self):
		"""Test query to db to get user from input of email."""

		result = self.client.get("/profile", follow_redirects=True)
		self.assertIn("Jane", result.data)


	def test_user_by_email(self):

		jane = get_user_by_email("jane@email.com")

		assert jane.lname == "Doe"


	def test_user_by_session(self):

		jane = get_user_by_session()

		assert jane.lname == "Doe"


	def test_is_favorited(self):

		jane = get_user_by_email("jane@email.com")

		assert is_favorited(jane, 1) is True
		assert is_favorited(jane, 2) is False


	def test_is_taken(self):

		jane = get_user_by_email("jane@email.com")

		assert is_taken(jane, 2) is True
		assert is_taken(jane, 1) is False



	def test_is_enrolled(self):

		jane = get_user_by_email("jane@email.com")

		assert is_enrolled(jane, 1) is False


	def test_search(self):
		"""Test for initial search results."""

		result = self.client.get("/search", data={"search": "biology"})
		self.assertIn("Advanced Biology", result.data)
		# self.assertNotIn("Art", result.data)


	def test_login(self):
		"""Test proper login process."""

		result = self.client.post("/login", data={"email": "jane@email.com", 
													"password": "pass"},
													follow_redirects=True)
		self.assertIn("Hi Jane", result.data)
		self.assertIn("Advanced Biology", result.data)
		self.assertIn("Intro to Art History", result.data)
		self.assertIn("You are currently not enrolled in any courses.", 
						result.data)


	def test_wrong_password(self):
		"""Test wrong password at login."""

		result = self.client.post("/login", data={"email": "jane@email.com", 
													"password": "notpass"},
													follow_redirects=True)
		self.assertNotIn("Hi Jane", result.data)
		self.assertIn("Incorrect password", result.data)


	def test_wrong_password(self):
		"""Test wrong password at login."""

		result = self.client.post("/login", data={"email": "notjane@email.com", 
													"password": "pass"},
													follow_redirects=True)
		self.assertNotIn("Hi Jane", result.data)
		self.assertIn("This email is not in our database", result.data)


	def test_register(self):
		"""Test login process."""

		result = self.client.post("/register", data={"fname": "John", 
													"lname": "Doe", 
													"email": "john@email.com", 
													"password": "pass"},
													follow_redirects=True)

		self.assertIn("You have successfully created an account", result.data)											
		self.assertIn("Hi John", result.data)
		self.assertNotIn("Advanced Biology", result.data)
		self.assertIn("You are currently not enrolled in any courses.", 
						result.data)
	

	def test_already_registered(self):
		"""Test failure to register when already a user."""

		result = self.client.post("/register", data={"fname": "Jane", 
													"lname": "Doe", 
													"email": "jane@email.com", 
													"password": "pass"},
													follow_redirects=True)

		self.assertIn("You already have an account", result.data)

	def test_lang_count(self):

		get_language_count("biology")
		assert lang_counts['en'] == 1
		assert lang_counts['zh'] == 0


	def test_bookmark(self):
		"""Test adding a course to enrolled."""

		result = self.client.post("/bookmark", 
								data={"current_user": "jane@email.com",
								"id": 1}, follow_redirects=True)
		self.assertIn("You have already added this", result.data)


	def test_bookmark(self):
		"""Test adding a course to enrolled."""

		result = self.client.post("/bookmark", 
								data={"current_user": "jane@email.com",
								"id": 2}, follow_redirects=True)
		self.assertIn("You have already added this", result.data)


	def test_unfavorite(self):
		"""Test removing a favorited course from database."""

		result = self.client.post("/unfavorite", 
								data={"current_user": "jane@email.com",
								"id": 1}, follow_redirects=True)
		self.assertIn("0", result.data)


	def test_logout(self):
		"""Test for logout."""

		result = self.client.get("/logout", follow_redirects=True)
		# self.assertEqual(result.status_code, 200)
		self.assertIn("You have successfully logged out.", result.data)


	def test_move_to_taken(self):
		"""Test moving course from fav to taken."""

		result = self.client.post("/move_to_taken", 
								data={"current_user": "jane@email.com",
								"id": 1, "origin": "fav"}, 
								follow_redirects=True)
		self.assertIn("0", result.data)


	def test_move_to_enrolled(self):
		"""Test moving course from fav to taking."""

		result = self.client.post("/move_to_enrolled", 
								data={"current_user": "jane@email.com",
								"id": 1}, follow_redirects=True)
		self.assertIn("0", result.data)


	def test_remove_from_taken(self):
		"""Test removing course from courses_taken table."""

		result = self.client.post("/remove_from_taken", 
								data={"current_user": "jane@email.com",
								"id": 2}, follow_redirects=True)
		self.assertIn("0", result.data)

if __name__ == '__main__':
    unittest.main()