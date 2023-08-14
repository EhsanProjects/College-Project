from sqlalchemy import *
from extentions import db


class Major(db.Model):
    __tablename__ = "majors"
    MajorID = Column(Integer, primary_key=True)
    MajorName = Column(VARCHAR(40), nullable=False, unique=True)

