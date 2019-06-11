from .. import db
from datetime import datetime
from flask import current_app
from app.models.roles import Role


class Publisher(db.Model):
    __tablename__ = "publishers"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120))
    overview = db.Column(db.String(2000))
    paypal = db.Column(db.String(120))
    logo = db.Column(db.String(120))
    banner = db.Column(db.String(120))
    physical_address = db.Column(db.String(120))
    postal_address = db.Column(db.String(120))
    association_membership = db.Column(db.String(120))
    rating = db.Column(db.Integer(), default=0)
    reg_certificate = db.Column(db.String(120))
    tax_registration = db.Column(db.String(120))
    operator_licence = db.Column(db.String(120))
    overal_ratings = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(
        db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    phones = db.relationship(
        "Pubphones", backref="profile", lazy="dynamic", cascade="all,delete-orphan"
    )
    emails = db.relationship(
        "Pubemails", backref="profile", lazy="dynamic", cascade="all,delete-orphan"
    )
    locations = db.relationship(
        "Publocations", backref="profile", lazy="dynamic", cascade="all,delete-orphan"
    )

    def getLocations(self):
        data = self.locations.group_by(Publocations.country)
        return data


class Pubphones(db.Model):
    __tablename__ = "pubphones"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(120))
    publisher_id = db.Column(db.Integer(), db.ForeignKey("publishers.id"))


class Pubemails(db.Model):
    __tablename__ = "pubemails"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    publisher_id = db.Column(db.Integer(), db.ForeignKey("publishers.id"))


class Publocations(db.Model):
    __tablename__ = "Publocations"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120))
    country = db.Column(db.String(120))
    publisher_id = db.Column(db.Integer(), db.ForeignKey("publishers.id"))

    def get_count(self):
        return (
            Publocations.query.filter_by(publisher_id=self.publisher_id)
            .group_by(Publocations.publisher_id)
            .count()
        )

    @staticmethod
    def get_country_code(country):
        from app.publisher.countries import get_arcode

        code = get_arcode()
        if country.lower().title() in code:
            county_code = code[country.lower().title()]
        else:
            county_code = "KE"

        return county_code
