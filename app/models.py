# -*- coding: utf-8 -*-

from mixins import CRUDMixin
from flask.ext.login import UserMixin
from sqlalchemy.orm import validates

from app import db


ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __init__(
            self,
            name=None,
            role=None):
        self.name = name
        self.role = role

    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    def __repr__(self):
        return '<User %r>' % (self.name)


class Style(CRUDMixin, db.Model):
    __tablename__ = 'styles'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True)
    # beers = db.relationship('Beer', backref='style', lazy='dynamic')

    def __init__(
            self,
            name=None):
        self.name = name

    def __repr__(self):
        return '<Style %r>' % (self.name)


class Brewery(CRUDMixin, db.Model):
    __tablename__ = 'breweries'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True)
    # beers = db.relationship('Beer', backref='style', lazy='dynamic')

    def __init__(
            self,
            name=None):
        self.name = name

    def __repr__(self):
        return '<Brewery %r>' % (self.name)


class Beer(CRUDMixin, db.Model):
    __tablename__ = 'beers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    brewery = db.relationship('Brewery')
    brewery_id = db.Column(db.Integer, db.ForeignKey('breweries.id'))
    name = db.Column(db.String(255))
    style = db.relationship('Style')
    style_id = db.Column(db.Integer, db.ForeignKey('styles.id'))
    abv = db.Column(db.Numeric(3,1))
    ba = db.Column(db.Integer)
    notes = db.Column(db.Text)

    def __init__(
            self,
            brewery=None,
            name=None,
            style=None,
            abv=None,
            ba=None,
            notes=None):
        self.brewery = brewery
        self.name = name
        self.style = style
        self.abv = abv
        self.ba = ba
        self.notes = notes

    def __repr__(self):
        return '<Beer %r %r>' % (self.brewery.name, self.name)


class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    user = db.relationship('User', uselist=False, backref='surveys')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    beer = db.relationship('Beer')
    beer_id = db.Column(db.Integer, db.ForeignKey('beers.id'))

    def __init__(
            self,
            rating=None,
            user=None,
            beer=None):
        self.rating = rating
        self.user = user
        self.beer = beer

    def __repr__(self):
        return '<Survey %r %r>' % (self.user.name, self.beer)
