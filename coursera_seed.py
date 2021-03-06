from sqlalchemy import func
from model import Course, Partner, CoursePartner, connect_to_db, db
from server import app
import requests

COURSERA_PARTNERS_URL = "https://api.coursera.org/api/partners.v1"


def load_coursera_partners():
    """Load partners from Coursera API responses into database"""

    partner_api_response = requests.get(COURSERA_PARTNERS_URL)

    partner_api_response = partner_api_response.json()

    partners = partner_api_response['elements']

    for partner in partners:
        partner_id = partner.get('id', '<unknown>')
        name = partner.get('name', '<unknown>')

        partner = Partner(partner_id=partner_id, name=name)

        db.session.add(partner)

    db.session.commit()


def load_coursera_courses():
    """Load courses from Coursera API responses into database."""

    print "Coursera courses"

    # Course.query.delete()

    i = 0
    while i < 21:
		num = str(i * 100)

		coursera_response = requests.get("https://api.coursera.org/api/courses.v1?start=" + num + "&fields=primaryLanguages,subtitleLanguages,certificates,description,startDate,workload,domainTypes,photoUrl,partnerIds")
		
		coursera_response = coursera_response.json()

		elements = coursera_response['elements']

		for element in elements:
			title = element.get('name', '<unknown>')
			description = element.get('description', '<unknown>')

			# course_type = element.get('courseType', '<unknown>')
			course_type = "instructor"

			slug = element.get('slug', '<unknown>')
			url = "https://www.coursera.org/learn/" + slug

			languages = element.get('primaryLanguages', '<unknown>')
			language =  "".join(languages)
			if "zh" in language:
				language = "zh"
			if "pt" in language:
				language = "pt"

			subtitles = element.get('subtitleLanguages', '<unknown>')
			subtitles = ", ".join(subtitles)

			workload = element.get('workload', '<unknown>')

			if element['certificates']:
				has_certificates = True
			else:
				has_certificates = False

			categories = element.get('domainTypes', '<unknown>')
			for item in categories:
				category = item.get('domainId', '<unknown>')
				subcategory = item.get('subdomainId', '<unknown>')

			picture = element.get('photoUrl', '<unknown>')

			partner_ids = element.get('partnerIds', '<unknown>')

			source = "Coursera"

			course = Course(title=title, course_type=course_type, description=description, url=url,
			language=language, subtitles=subtitles, workload=workload, 
			has_certificates=has_certificates, category=category, subcategory=subcategory,
			picture=picture, source=source)

			for partner_id in partner_ids:
				try:
					partner = Partner.query.filter_by(partner_id=partner_id).one()
					course.partners.append(partner)
				except:
					pass

			db.session.add(course)

		i = i + 1
		
		db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_coursera_partners()
    load_coursera_courses()