from sqlalchemy import *
from extentions import db
from datetime import datetime
import datetime
class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:

            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
        return value
class Student(db.Model):
    __tablename__ = "students"
    StudentID = Column(INTEGER, primary_key=True)
    LastName = Column(VARCHAR(25), nullable=False)
    FirstName = Column(VARCHAR(25), nullable=False)
    Major = Column(VARCHAR(20), nullable=False)
    EnrollmentDate = Column(MyDateTime, default=datetime.datetime.now, nullable=False)
    GraduationDate = Column(MyDateTime, nullable=True)
#Column(MyDateTime, default=datetime.datetime.now)
#EnrollmentDate = Column(DATETIME, nullable=False, DEFAULT=now)
#DT = Column(DateTime(timezone=True), default=func.now())
#EnrollmentDate = Column(DATETIME, nullable=True, default=datetime.now())