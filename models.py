from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

courses_students = db.Table(
    'courses_students',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Course(db.Model, SerializerMixin):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    credits = db.Column(db.Integer, nullable=False)

    # Relationship to Student
    students = db.relationship(
        'Student',
        secondary=courses_students,
        back_populates='courses'
    )

class Student(db.Model, SerializerMixin):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Relationship to Course
    courses = db.relationship(
        'Course',
        secondary=courses_students,
        back_populates='students'
    )