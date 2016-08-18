from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
	"""Course model."""

	__tablename__ = "courses"

	course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String, nullable=False)
	category = db.Column(db.String(1000))
	subcategory = db.Column(db.String(1000))
	price = db.Column(db.Integer, default=0)
	course_type = db.Column(db.String, default="self")
	source = db.Column(db.String, nullable=False)
	description = db.Column(db.Text)
	languages = db.Column(db.String(100))
	subtitles = db.Column(db.String(100))
	workload = db.Column(db.String(200))
	has_certificates = db.Column(db.Boolean, default=False)
	url = db.Column(db.String(500))
	picture = db.Column(db.String(500))

	def __repr__(self):
		return "<Course id=%s, title=%s>" % (self.course_id, self.title)


class Partner(db.Model):
	"""Partner mode."""

	__tablename__ = "partners"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	partner_id = db.Column(db.String(10), nullable=False, unique=True)
	name = db.Column(db.String(400), nullable=False)

	courses = db.relationship('Course', secondary="courses_partners", backref='partners')

	def __repr__(self):
		return "<Partner id=%s, name=%s>" % (self.partner_id, self.name)


class CoursePartner(db.Model):
	"""Association table for Course and Partner models."""

	__tablename__ = "courses_partners"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	partner_id = db.Column(db.String(10), db.ForeignKey('partners.partner_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<partner_id=%s, course_id=%s>" % (self.partner_id, self.course_id)


class User(db.Model):
	"""Table for User models."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	fname = db.Column(db.String(20), nullable=False)
	lname = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return "<User id=%s, fname=%s, lname=%s>" % (self.user_id, self.fname, self.lname)


class Courses_Favorited(db.Model):
	"""Table for Courses favotited by Users."""

	__tablename__ = "courses_favorited"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<Favorite user_id=%s, course_id=%s>" % (self.user_id, self.course_id)


class Courses_Taken(db.Model):
	"""Table for Courses taken by Users."""

	__tablename__ = "courses_taken"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<Taken user_id=%s, course_id=%s>" % (self.user_id, self.course_id)


class Courses_Taking(db.Model):
	"""Table for Courses currently being taken by Users."""

	__tablename__ = "courses_taking"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)

	def __repr__(self):
		return "<Taking user_id=%s, course_id=%s>" % (self.user_id, self.course_id)


class Ratings(db.Model):
	"""Table for Ratings of Courses made by Users."""

	__tablename__ = "courses_ratings"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
	rating = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return "<user_id=%s, course_id=%s, rating=%s>" % (self.user_id, self.course_id, self.rating)


def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///courses'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."