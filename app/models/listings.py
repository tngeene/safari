from datetime import datetime
from app.models.bookings import Booking
from app.models.places import Place
from app.models.prices import Price
from sqlalchemy import or_, and_
from flask import current_app
from .. import db
from .reviews import Review
from sqlalchemy.ext.hybrid import hybrid_method

listing_tags = db.Table('listing_tags',
                        db.Column('listing_id', db.Integer, db.ForeignKey('listings.id')),
                        db.Column('category_id', db.Integer, db.ForeignKey('categories.id')))


class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default='')
    short_description = db.Column(db.String(320), default='')
    long_description = db.Column(db.String(2000), default='')
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location = db.Column(db.String(80), index=True)
    duration = db.Column(db.Integer)
    package = db.Column(db.String(64), index=True)
    rating = db.Column(db.Integer(), default=0)
    overal_ratings = db.Column(db.Integer(), default=0)
    connectivity = db.Column(db.String(120))
    physical_condition = db.Column(db.String(64))
    price_type_id = db.Column(db.Integer(), db.ForeignKey('prices.id'))
    availability_from = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    availability_to = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    feature_id = db.Column(db.Integer, db.ForeignKey('features.id'))
    add_ons = db.Column(db.String(2000), default='')
    policy = db.Column(db.String(2000), default='')
    status = db.Column(db.Boolean(), index=True, default=False)
    published = db.Column(db.Boolean(), index=True, default=False)
    space = db.Column(db.Integer())

    # Relationships
    bookings = db.relationship('Booking', backref='listing', lazy='dynamic')
    reviews = db.relationship('Review', backref='listing', lazy='dynamic')
    images = db.relationship('Image', backref='listing', lazy='dynamic')
    activities = db.relationship('Activity', backref='listing', lazy='dynamic')
    places = db.relationship('Place', backref='listing', lazy='dynamic')
    days = db.relationship('Day', backref='listing', lazy='dynamic')
    categories = db.relationship('Category', secondary=listing_tags, backref='listings', lazy='dynamic')

    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_bookings_count(self):
        count = Booking.query.filter_by(listing_id=self.id).count()
        return count

    def get_listings(self):
        return Review.query.filter_by(listing_id=self.id)

    def get_country_count(self):
        data = Listing.query.filter_by(publisher=self.publisher, location=self.location).count()
        return data

    @hybrid_method
    def child_count(self):
        return len([_child for _child in self.bookings])


def get_search(name, date, page):
    if name != '':
        first = Listing.query.filter(db.false())
        list = [(row.listing_id) for row in Place.query.filter(Place.place.like('%' + name.lower() + '%')).all()]
        if list:
            first = Listing.query.filter(Listing.id.in_(list)).filter(Listing.availability_to > date).filter(Listing.status == True)
        own = Listing.query.filter(
            and_(Listing.location.like('%' + name.capitalize() + '%'), Listing.availability_to > date)).filter(Listing.status == True)
        listings = first.union(own).order_by(Listing.rating.desc()).paginate(page,
                                                                                current_app.config['POSTS_PER_PAGE'],
                                                                                False)
    else:
        listings = Listing.query.filter(Listing.availability_to > date).filter(Listing.status == True).order_by(Listing.rating.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)

    return listings


def get_range(maxval, minval, page):
    listings = Listing.query.filter(db.false())
    list = [(row.id) for row in
            Price.query.filter(and_(Price.total_price_adults <= maxval, Price.total_price_adults >= minval)).all()]
    if list:
        listings = Listing.query.filter(Listing.price_type_id.in_(list)).filter(Listing.status == True)
    return listings.order_by(Listing.createdAt.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)


def get_ratings(data, page):
    list = []
    for field in ['first', 'second', 'third', 'fourth', 'fifth']:
        if field in data:
            list.append(int(data[field]))
    listings = Listing.query.filter(Listing.status == True)
    if list:
        listings = Listing.query.filter(Listing.rating.in_(list)).filter(Listing.status == True)
    return listings.order_by(Listing.createdAt.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
