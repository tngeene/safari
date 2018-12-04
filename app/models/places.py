
from .. import db


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(120))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
