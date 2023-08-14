from sqlalchemy import *
from decimal import Decimal

from sqlalchemy.orm import backref

from extentions import db


class Studentcourse(db.Model):
    __tablename__ = "studentcourses"

    StudentID = Column(Integer, ForeignKey("students.StudentID", ondelete="cascade", onupdate="cascade"),
                       primary_key=True, nullable=True)
    CourseID = Column(Integer, ForeignKey("courses.CourseID", ondelete="cascade", onupdate="cascade"), primary_key=True,
                      nullable=False)

    student = db.relationship('Student', backref=backref('studentcourses', lazy='dynamic'))
    course = db.relationship('Course', backref=backref('studentcourses', lazy='dynamic'))