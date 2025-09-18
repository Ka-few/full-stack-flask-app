from flask import Flask, request, make_response
from flask_restful import Resource, Api
from models import db, Course, SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compct = False
db.init_app(app)
api = Api(app)


class CourseResource(Resource, SerializerMixin):
    serialize_rules = ('courses_students',) 

    def get(self, course_id=None):
        if course_id:
            course = Course.query.get(course_id)
            if course:
                return make_response(course.to_dict(), 200)
            return make_response({"error": "Course not found"}, 404)
        else:
            courses = Course.query.all()
            return make_response([course.to_dict() for course in courses], 200)

    def get_by_id(self, course_id):
        course = Course.query.get(course_id)
        if course:
            return make_response(course.to_dict(), 200)
        return make_response({"error": "Course not found"}, 404)

    def post(self):
        data = request.get_json()
        new_course = Course(
            name=data.get('name'),
            description=data.get('description'),
            credits=data.get('credits')
        )
        db.session.add(new_course)
        db.session.commit()
        return make_response(new_course.to_dict(), 201)

    def put(self, course_id):
        data = request.get_json()
        course = Course.query.get(course_id)
        if not course:
            return make_response({"error": "Course not found"}, 404)

        course.name = data.get('name', course.name)
        course.description = data.get('description', course.description)
        course.credits = data.get('credits', course.credits)

        db.session.commit()
        return make_response(course.to_dict(), 200)

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return make_response({"error": "Course not found"}, 404)

        db.session.delete(course)
        db.session.commit()
        return make_response({}, 204)