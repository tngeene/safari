from datetime import datetime

from .. import db


class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120))
    location=db.Column(db.String(120))
    total_price_adults = db.Column(db.Numeric)
    total_price_children = db.Column(db.Numeric)
    price_per_day_children = db.Column(db.Numeric)
    price_per_day_adults = db.Column(db.Numeric)
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    offers = db.relationship('Offer', backref='price')
    listing = db.relationship('Listing', backref='price',uselist=False)
    includes = db.relationship('Include', backref='price',lazy='dynamic')
