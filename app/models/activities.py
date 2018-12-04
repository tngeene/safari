
from .. import db


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(120))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
