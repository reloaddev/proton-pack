from .. import db

class Ghost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))