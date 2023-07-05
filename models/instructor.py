from sqlalchemy import *
from decimal import Decimal
from extentions import db

from datetime import datetime
import datetime
class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:

            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
        return value
class Instructor(db.Model):
    __tablename__ = "instructors"
    InstructorID = Column(INTEGER, primary_key=True)
    LastName = Column(VARCHAR(25), nullable=False)
    FirstName = Column(VARCHAR(25), nullable=False)
    Status = Column(CHAR(1), nullable=True)
    DepartmentChairman = Column(Boolean, nullable=True)
    HireDate = Column(MyDateTime, default=datetime.datetime.now, nullable=True)
    AnnualSalary = Column(Numeric(10, 2), nullable=True)
    DepartmentID = Column(INTEGER, nullable=True)
    #DepartmentID = Column(INTEGER, ForeignKey("departments.DepartmentID", ondelete="cascade", onupdate="cascade"),
     #                     nullable=True)




