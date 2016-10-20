# -*- coding: utf-8 -*-

from mixins import CRUDMixin
from flask.ext.login import UserMixin

from app import db


ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, CRUDMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    s1 = db.Column(db.Boolean)

    def __init__(
            self,
            name=None,
            userid=None,
            role=None,
            s1=False):
        self.name = name
        self.userid = userid
        self.role = role
        self.s1 = s1

    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Survey1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False, backref='survey1')

    def __init__(
            self,
            rating=None):
        self.rating=rating

    def get_id(self):
        return unicode(self.id)
