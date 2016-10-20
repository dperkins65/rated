# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, fields, validators, Required, Email, Regexp
from models import User
from app import db


class LoginForm(Form):
    name = fields.TextField(validators=[Required()])

    def get_user(self):
        return db.session.query(User).filter_by(name=self.name.data).first()


class Survey1Form(Form):
    rating = fields.RadioField('Rating',
        choices=[('1', 'One Point'), ('2', 'Two Points'),
            ('3', 'Three Points'), ('4', 'Four Points'), ('5', 'Five Points')],
        validators=[Required()], default=None)

