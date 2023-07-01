from sqlalchemy import *
from decimal import Decimal
from extentions import db

class Course(db.Model):
    __tablename__ = "courses"
    CourseID = Column(Integer, primary_key=True)
    CourseNumber = Column(Integer, nullable=False)
    CourseDescription = Column(VARCHAR(50), nullable=False)
    CourseUnits = Column(Integer, nullable=False)
    DepartmentID = Column(db.Integer, ForeignKey("departments.DepartmentID", ondelete="cascade", onupdate="cascade"),
                          nullable=False)
    InstructorID = db.Column(Integer, ForeignKey("instructors.InstructorID", ondelete="cascade", onupdate="cascade"),
                             nullable=False)
