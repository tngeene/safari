from datetime import datetime
from .. import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    card_holder_name = db.Column(db.String(64), index=True)
    card_number = db.Column(db.String(64), index=True)
    select_card = db.Column(db.String(64), index=True)
    month = db.Column(db.String(64), index=True)
    years = db.Column(db.String(64), index=True)
    card_identification_number = db.Column(db.String(64), index=True)
    billing_zip_code = db.Column(db.String(64), index=True)
    amount = db.Column(db.Numeric)
    status = db.Column(db.Boolean(), index=True, default=False)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    booking_id = db.Column(db.Integer(), db.ForeignKey('bookings.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

