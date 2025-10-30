from ghostbusters_wiki import db
from sqlalchemy import Column, Date, Integer, Text

class Human(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True)
    hire_date = Column(Date, nullable=False)