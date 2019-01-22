from datetime import datetime

from .. import db
from flask_moment import Moment


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer(), db.ForeignKey('listings.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    status = db.Column(db.Boolean(), index=True, default=False)
    state = db.Column(db.String(120), default='pending')
    reason = db.Column(db.String(300), default='')
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    # primary keys
    offers = db.relationship('Offer', backref='booking')
    payments = db.relationship('Payment', backref='booking')
    orders = db.relationship('Order', backref='booking', uselist=False)

    def get_time(self):
        return self.createdAt
