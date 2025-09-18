from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Course

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


class Home(Resource):
    def get(self):
        return make_response({"message": "Welcome to the Course API"}, 200)


# Collection resource (/courses)
class Courses(Resource):
    def get(self):
        courses = Course.query.all()
        return make_response([course.to_dict() for course in courses], 200)

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


# Single resource (/courses/<id>)
class CourseByID(Resource):
    def get(self, course_id):
        course = Course.query.get(course_id)
        if course:
            return make_response(course.to_dict(), 200)
        return make_response({"error": "Course not found"}, 404)

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


# Register routes
api.add_resource(Home, '/')
api.add_resource(Courses, '/courses')
api.add_resource(CourseByID, '/courses/<int:course_id>')


if __name__ == "__main__":
    app.run(debug=True)
