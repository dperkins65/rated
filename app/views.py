# -*- coding: utf-8 -*-

import uuid
from datetime import date
from flask import render_template, flash, redirect
from flask import url_for, g, request
from flask.views import View
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries
from models import User, Survey1
from forms import LoginForm, Survey1Form
from config import DATABASE_QUERY_TIMEOUT
from app import app, db, lm
from decorators import admin_required

@app.route('/survey_1/', methods=['GET', 'POST'])
@login_required
def survey_1():
    g.user = current_user
    if g.user.s1 is False:
        form = Survey1Form(request.form)
        if form.validate_on_submit():
            survey = Survey1()
            form.populate_obj(survey)
            survey.user = g.user
            db.session.add(survey)
            g.user.s1 = True
            db.session.commit()
            return redirect(request.args.get("next") or url_for("index"))
        return render_template('survey/Survey1.html', title='Survey', form=form)
    else:
        return redirect(url_for('index'))


# class SurveyView(View):
#     methods = ['GET', 'POST']
#
#     def survey():
#         g.user = current_user
#         form = SurveyForm(request.form)
#         if form.validate_on_submit():
#             survey_model = SurveyModel()
#             form.populate_obj(survey_model)
#             survey_model.user = g.user
#             db.session.add(survey_model)
#             #find a new way to detect that a survey has been completed, instead of a new way to mark it.
#             db.session.commit()
#             return redirect(request.args.get("next") or url_for("index"))















#TODO: Redirect to final
# return render_template("final.html", title='Top Secret - Dharma Initiative: Task Force Echo - Human Trials 0014')





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


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    if user.is_admin():
        return redirect(url_for('admin'))
    return render_template("index.html", title="Home", user=user)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
                (query.statement, query.parameters, query.duration, query.context))
    return response


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error))


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
