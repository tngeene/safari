from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from .. import db, login_manager


class Permission:
    USER = 0x01
    CUSTOMER = 0x07
    PUBLISHER = 0x08
    CAN_LIKE = 0x01
    CAN_POST = 0x02
    CAN_EDIT = 0x04
    CAN_REMOVE = 0x08
    ADMINISTRATOR = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    createdAt = db.Column(db.DateTime(), default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USER, '', True),
            'Customer': (Permission.CUSTOMER, 'customer', True),
            'Publisher': (Permission.PUBLISHER, 'publisher', True),
            'Administrator': (
                Permission.ADMINISTRATOR,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name
