# -*- coding: utf-8 -*-

import uuid
from flask import render_template, flash, redirect
from flask import url_for, g, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries

from app import app, db, lm
from app.models import User
from app.forms import LoginForm, Survey1Form

from config import DATABASE_QUERY_TIMEOUT


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    if user.is_admin():
        return redirect(url_for('admin'))
    return render_template("index.html", title="Home", user=user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        try:
            user = form.get_user()
            login_user(user)
        except: #TODO fix exception type/reason
            user = User(name=form.name.data, userid=(str(uuid.uuid1())))
            db.session.add(user)
            db.session.commit()
            login_user(user)
        user = g.user
        if current_user.is_admin():
            return redirect(url_for('admin'))
        else:
            return redirect(request.args.get("next") or url_for("index"))
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                (query.statement, query.parameters, query.duration, query.context))
    return response


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error))
