from ghostbusters_wiki import db
from sqlalchemy import Column, Integer, Text, BigInteger


class Ghost(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    spooky_level = Column(Integer, nullable=False)
    ectoplasm_volume = Column(BigInteger)
    reporter_id = Column(BigInteger)
    danger_rating = Column(Integer)