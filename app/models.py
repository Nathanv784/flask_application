from db import db
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
#from app import db

#db = SQLAlchemy()
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    

    

    notes = db.relationship('Notes', backref='student', lazy=True)

    def __init__(self, firstname, lastname, email):
        if not firstname or not lastname:
            raise ValueError("Both firstname and lastname must be provided and not empty.")
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    @validates('email')
    def validate_email(self, key, address):
        # Validate that the address is a well-formed email address
        if '@' not in address:
            raise ValueError('Invalid email address')
        return address

    def __repr__(self):
        return f'<Student {self.firstname} {self.lastname}>'

    @classmethod
    def init_db(cls, app):
        db.init_app(app)
        with app.app_context():
            db.create_all()

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    marks = db.Column(db.Integer, nullable=True)
    

    def __repr__(self):
        return f'<Note {self.id} for Student {self.student_id}>'
    