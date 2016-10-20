# -*- coding: utf-8 -*-

import os
from datetime import timedelta
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=240)

from app.views import admin
from app.views import general
from app.views import survey

import models
