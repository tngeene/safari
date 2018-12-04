from datetime import datetime

from .. import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer(), db.ForeignKey('bookings.id'))

    children = db.Column(db.Integer, default=1)
    adults = db.Column(db.Integer, default=1)
    grand_total = db.Column(db.Numeric)
    departure_date = db.Column(db.DateTime(), default=datetime.utcnow)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)


