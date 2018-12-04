from datetime import datetime

from .. import db


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(64), index=True)
    listing_id = db.Column(db.Integer(), db.ForeignKey('listings.id'))
    publisher_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    value = db.Column(db.Integer, default=0)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
