from sqlalchemy import *
from decimal import Decimal
from extentions import db


class Instructor(db.Model):
    __tablename__ = "instructors"
    InstructorID = Column(INTEGER, primary_key=True)
    LastName = Column(VARCHAR(25), nullable=False)
    FirstName = Column(VARCHAR(25), nullable=False)
    Status = Column(CHAR(1), nullable=False)
    DepartmentChairman = Column(Boolean, nullable=False)
    HireDate = Column(DATE, nullable=False)
    AnnualSalary = Column(Numeric(10, 2), nullable=False)
    DepartmentID = Column(INTEGER, ForeignKey("departments.DepartmentID", ondelete="cascade", onupdate="cascade"),
                          nullable=False)
