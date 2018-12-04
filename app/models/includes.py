from .. import db


class Include(db.Model):
    __tablename__ = 'includes'
    id = db.Column(db.Integer, primary_key=True)
    include = db.Column(db.String(120))
    price_id = db.Column(db.Integer, db.ForeignKey('prices.id'))
