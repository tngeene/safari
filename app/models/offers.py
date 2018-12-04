from datetime import datetime

from .. import db


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    price_id = db.Column(db.Integer(), db.ForeignKey('prices.id'))
    booking_id = db.Column(db.Integer(), db.ForeignKey('bookings.id'))
    description = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
