from datetime import datetime
from flask import current_app
from .. import db
from app.models.listings import Listing,listing_tags

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    image_url = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_count(self):
        data = Listing.query.join(
            listing_tags, (listing_tags.c.listing_id == Listing.id)).filter(
                listing_tags.c.category_id == self.id).filter(Listing.status == True)
        return data.count()

def get_categories(data,page):
    list=[]
    for field in [(row.name) for row in Category.query.all()]:
        if field in data:
            list.append(int(data[field]))
    listings=Listing.query.filter(Listing.status == True).order_by(Listing.createdAt.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    if list:
        listings = Listing.query.join(
            listing_tags, (listing_tags.c.listing_id == Listing.id)).filter(
                listing_tags.c.category_id.in_(list)).filter(Listing.status == True).order_by(Listing.createdAt.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    return listings
