# models.py

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    courses = db.relationship('Course', secondary='enrollment', backref='students')


    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
    
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')


    