from datetime import datetime
from .. import db


class Disclaimer(db.Model):
    __tablename__ = "disclaimers"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return "<Disclaimer '%s'>" % self.name
