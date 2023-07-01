from sqlalchemy import *
from extentions import db


class Department(db.Model):
    __tablename__ = "departments"
    DepartmentID = Column(Integer, primary_key=True)
    DepartmentName = Column(VARCHAR(40), nullable=False, unique=True)

