from datetime import datetime

from .. import db


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    body = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)
