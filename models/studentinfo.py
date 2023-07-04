from sqlalchemy import *
from extentions import db

class StudentInfo(db.Model):
    __tablename__ = "studentinfo"
    ID = Column(INTEGER, primary_key=True)
    Dob = Column(DATE, nullable=False)
    Phone = Column(CHAR(10), nullable=False)
    Address = Column(VARCHAR(50), nullable=False)
    City = Column(VARCHAR(30), nullable=False)
    State = Column(CHAR(2), nullable=False)
    Zipcode = Column(CHAR(5), nullable=False)
    Email = Column(VARCHAR(50), nullable=False)
    StudentID = Column(Integer, ForeignKey("students.StudentID", ondelete="cascade", onupdate="cascade"),
                       primary_key=True, nullable=False)
