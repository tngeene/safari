from .. import db


class Day(db.Model):
    __tablename__ = 'days'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    day_by_day = db.Column(db.String(2000), default='')
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
