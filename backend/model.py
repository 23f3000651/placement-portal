from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import UniqueConstraint

from enum import Enum
from datetime import datetime

db = SQLAlchemy()

class Role(Enum):
    ADMIN = 'admin'
    COMPANY= 'company'
    STUDENT = 'student'

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(15),nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company = db.relationship("Company", backref="user",uselist=False, lazy=True)
    student = db.relationship("Student", backref="user", uselist=False,lazy=True)

class Company(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(200))
    website = db.Column(db.String(200))
    approval_status = db.Column(db.Boolean, default=False)
    drives = db.relationship("PlacementDrive", backref="company", lazy=True)
    
    

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    Student_name=db.Column(db.String(150), nullable=False)
    education = db.Column(db.String(200))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    resume_link = db.Column(db.String(255)) 
    applications = db.relationship("Application", backref="student", lazy=True)
    interviews = db.relationship('Interview', backref='student', lazy=True)

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey("company.id"),nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text)
    eligibility_criteria = db.Column(db.Text, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable=False)
    is_active=db.Column(db.Boolean,default=True)
    applications = db.relationship("Application", backref="drive", lazy=True)


    def to_json(self):
        return {
            "id": self.id,
            
            "company_id":self.company_id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "eligibility_criteria": self.eligibility_criteria,
            "application_deadline": str(self.application_deadline),
            "is_active":self.is_active
        }
    
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id=db.Column( db.Integer,db.ForeignKey("student.id"),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey('placement_drive.id'), nullable=False)
    status = db.Column(db.String(20), default="Applied")
    interviews = db.relationship('Interview', backref='application', lazy=True)


    
    

    
    __table_args__ = (
        UniqueConstraint('student_id', 'drive_id', name='unique_student_drive'),
    )
class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    interview_date = db.Column(db.Date)
    interview_time = db.Column(db.String(50))
    status = db.Column(db.String(50), default="SCHEDULED")
    feedback = db.Column(db.Text)
    offer_letter = db.Column(db.String(255))
    placed = db.Column(db.Boolean, default=False)
    company = db.relationship("Company", backref="interviews")

