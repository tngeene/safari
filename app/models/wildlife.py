from datetime import datetime

from .. import db


class Wildlife(db.Model):
    __tablename__ = 'wildlife'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(500), index=True)
    image_url = db.Column(db.String(64), index=True)
    frequency = db.Column(db.String(80), index=True)
    park_id = db.Column(db.Integer(), db.ForeignKey('parks.id'), index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Wildlife \'%s\'>' % self.name
