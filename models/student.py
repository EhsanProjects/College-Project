from sqlalchemy import *
from sqlalchemy.orm import backref
from sqlalchemy import Column, DateTime
from datetime import datetime, date
from sqlalchemy import Column, Date, DateTime, ForeignKey, VARCHAR

from extentions import db
from sqlalchemy import TypeDecorator, DateTime
from datetime import datetime


class MyDateTime(Column):
    def __init__(self, *args, **kwargs):
        kwargs['type_'] = DateTime
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.strftime('%Y-%m-%d %H:%M:%S')

class Student(db.Model):
    __tablename__ = "students"
    StudentID = Column(INTEGER, primary_key=True)
    LastName = Column(VARCHAR(25), nullable=False)
    FirstName = Column(VARCHAR(25), nullable=False)

    # Major = Column(VARCHAR(20), nullable=False)
    EnrollmentDate = MyDateTime(nullable=False, default=datetime.now)
    GraduationDate = MyDateTime(nullable=True)
    MajorID = Column(INTEGER, ForeignKey("majors.MajorID", ondelete="cascade", onupdate="cascade"),
                          nullable=False)
    major = db.relationship('Major', backref=backref('students', lazy='dynamic'))

#Column(MyDateTime, default=datetime.datetime.now)
#EnrollmentDate = Column(DATETIME, nullable=False, DEFAULT=now)
#DT = Column(DateTime(timezone=True), default=func.now())
#EnrollmentDate = Column(DATETIME, nullable=True, default=datetime.now())