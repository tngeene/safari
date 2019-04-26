from datetime import datetime

from .. import db


class Park(db.Model):
    __tablename__ = 'parks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(10000))
    image_url = db.Column(db.String(64), index=True)
    climate = db.Column(db.String(500), index=True)
    best_time_to_visit = db.Column(db.String(500))
    country_id = db.Column(db.Integer(), db.ForeignKey('countries.id'), index=True)
    wildlife = db.relationship('Wildlife', backref='park', lazy='dynamic')
    birds = db.relationship('Bird', backref='park', lazy='dynamic')
    price_type_id = db.Column(db.Integer(), db.ForeignKey('prices.id'))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Park \'%s\'>' % self.name
