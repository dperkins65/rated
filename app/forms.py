# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, fields, validators, Required, Email, Regexp
from models import User, Brewery, Beer, Style
from app import db


class LoginForm(Form):
    name = fields.TextField(validators=[Required()])

    def get_user(self):
        return db.session.query(User).filter_by(name=self.name.data).first()


class SurveyForm(Form):
    rating = fields.RadioField('Rating',
        choices=[('1', 'One Point'), ('2', 'Two Points'),
            ('3', 'Three Points'), ('4', 'Four Points'), ('5', 'Five Points')],
        validators=[Required()], default=None)


class AddStyleForm(Form):
    name = fields.TextField(u"Style", validators=[Required()], default=None)


class AddBreweryForm(Form):
    name = fields.TextField(u"Brewery", validators=[Required()], default=None)


class AddBeerForm(Form):
    brewery = fields.SelectField(u"Brewery", validators=[Required()], coerce=int)
    name = fields.TextField(u"Beer Name", validators=[Required()])
    style = fields.SelectField(u"Beer Style", validators=[Required()], coerce=int)
    abv = fields.DecimalField(u"%ABV", default=0)
    ba = fields.IntegerField(u"BeerAdvocate Rating", default=0)
    notes = fields.TextAreaField(u'Additional Notes')
