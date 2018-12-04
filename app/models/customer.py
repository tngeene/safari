from .. import db
from datetime import datetime

class Customer(db.Model):

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120))
    overview = db.Column(db.String(2000))
    paypal = db.Column(db.String(120))
    logo = db.Column(db.String(120))
    banner = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    twitter = db.Column(db.String(120))
    instagram = db.Column(db.String(120))

    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
