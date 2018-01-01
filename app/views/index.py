from flask import Blueprint, render_template, g, redirect, url_for
from flask_login import login_required, current_user

from app.database import Model, Survey


mod = Blueprint('index', __name__)


@mod.route('/')
def root():
    if current_user.is_authenticated:
         return redirect(url_for('index.index'))
    else:
         return redirect(url_for('user.login'))


@mod.route('/index/')
@login_required
def index():
    user = g.user
    if user.is_admin:
        return redirect(url_for('admin.admin'))
    models = Model.query.all()
    completed_surveys = Survey.query.filter(Survey.user == user).all()
    surveyed_models = [x.model for x in completed_surveys]
    return render_template("index.html",
                           user=user,
                           models=models,
                           surveyed_models=surveyed_models)
