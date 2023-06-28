from sqlalchemy import *
from extentions import db

class Student(db.Model):
    __tablename__ = "students"
    StudentID = Column(INTEGER, primary_key=True)
    LastName = Column(VARCHAR(25), nullable=False)
    FirstName = Column(VARCHAR(25), nullable=False)
    EnrollmentDate = Column(DATETIME, nullable=False)
    GraduationDate = Column(DATETIME, nullable=True)

