from datetime import datetime

from .. import db


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    image_url = db.Column(db.String(64), index=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

