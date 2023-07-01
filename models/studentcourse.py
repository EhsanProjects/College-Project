from sqlalchemy import *
from decimal import Decimal
from extentions import db


class studentcourse(db.Model):
    __tablename__ = "studentcourses"

    StudentID = Column(Integer, ForeignKey("students.StudentID", ondelete="cascade", onupdate="cascade"),
                       primary_key=True, nullable=False)
    CourseID = Column(Integer, ForeignKey("courses.CourseID", ondelete="cascade", onupdate="cascade"), primary_key=True,
                      nullable=False)

