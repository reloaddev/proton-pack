from ghostbusters_wiki import db
from sqlalchemy import Column, Integer, Text, BigInteger, ForeignKey


class Ghost(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    spooky_level = Column(Integer, nullable=False)
    ectoplasm_volume = Column(BigInteger)
    reporter_id = Column(BigInteger, ForeignKey("human.id"), nullable=False)
    danger_rating = Column(Integer)