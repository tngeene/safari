from datetime import datetime

from .. import db


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(500), index=True)
    image_url = db.Column(db.String(64), index=True)
    overview = db.Column(db.String(500), index=True)
    climate = db.Column(db.String(500), index=True)
    best_time_to_visit = db.Column(db.String(500))
    parks = db.relationship('Park', backref='country', lazy='dynamic')
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Country \'%s\'>' % self.name
