# -*- coding: utf-8 -*-

from flask import render_template
from flask.ext.login import login_required

from app import app
from app.decorators import admin_required
from app.models import User, Survey1


@app.route('/admin')
@login_required
@admin_required
def admin():
    users = User.query.filter_by(role=0)
    return render_template('admin/index.html', title="Admin", users=users)


@app.route('/admin_survey1/')
@login_required
@admin_required
def admin_survey1():
    surveys = Survey1.query.all()
    return render_template('admin/partials/survey1.html', title='Admin Survey-1', surveys=surveys)
