from __future__ import division

import numpy, sys, json
from operator import itemgetter

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required

from sqlalchemy import func, exc, desc

from app.database import db, User, Survey, Model, Make
from app.decorators import admin_required
from app.forms import AddModelForm, AddMakeForm


mod = Blueprint('admin', __name__)


@mod.route('/admin/')
@mod.route('/admin/index/')
@login_required
@admin_required
def admin():
    return render_template('admin/index.html')


@mod.route('/admin/log/')
@login_required
@admin_required
def log():
    log = {x:'' for x in Model.query.all()}
    for model in list(log.keys()):
        surveys = Survey.query.filter_by(model_id=model.id)
        users = User.query.filter_by(role=0)
        try:
            percent_complete = int(surveys.count() / users.count() * 100)
        except ZeroDivisionError:
            percent_complete = int(0)
        submitted = [x.user.name for x in surveys]
        not_submitted = [x.name for x in users if x.name not in submitted]
        log[model] = {
            'submitted': submitted,
            'not_submitted': not_submitted,
            'percent_complete': percent_complete,
            }
    return render_template('admin/log.html', log=log)


def calculate_results():
    results = []
    models = Model.query.all()
    for model in models:
        surveys = Survey.query.filter_by(model=model)
        ratings_list = [survey.rating for survey in surveys if survey.model == model]
        if not ratings_list:
            ratings_list = [0]
        try:
            ratings_range = (min(ratings_list), max(ratings_list))
        except ValueError:
            ratings_range = (int(0), int(0))
        ratings_array = numpy.array(ratings_list)
        results.append({'make_name': model.make.name,
                        'model_id': model.id,
                        'model_name': model.name,
                        'model_vintage': model.vintage.strftime('%b %d, %Y') if model.vintage != None else model.vintage,
                        'model_notes': model.notes,
                        'ratings_mean': numpy.nan_to_num(numpy.around(numpy.mean(ratings_array, axis=0), decimals=2)),
                        'ratings_std': numpy.nan_to_num(numpy.around(numpy.std(ratings_array, axis=0), decimals=2)),
                        'ratings_range': ratings_range,
                        'user_ratings': [{'user': survey.user.name,
                                         'rating': survey.rating} for survey in surveys if survey.model == model],
                        })
    return sorted(results, key=itemgetter('ratings_mean'))


@mod.route('/admin/results/')
@login_required
@admin_required
def results():
    results = calculate_results()
    return render_template('admin/results.html', results=results)


@mod.route('/admin/result/<int:model_id>')
@login_required
@admin_required
def result(model_id):
    surveys = Survey.query.filter_by(model_id=model_id).order_by(desc('rating'))
    results = calculate_results()
    result = [x for x in results if x['model_id'] == model_id][0]
    results.reverse()
    suf = lambda n: "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))
    rank = suf(results.index(result) + 1)
    return render_template('admin/result.html', surveys=surveys, result=result, rank=rank)


@mod.route('/admin/configuration/')
@login_required
@admin_required
def configuration():
    models = Model.query.all()
    return render_template('admin/configuration.html', models=models)


@mod.route('/admin/configuration/add_make/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_make():
    form = AddMakeForm()
    if form.validate_on_submit():
        make = Make()
        form.populate_obj(make)
        db.session.add(make)
        try:
            db.session.commit()
            flash(u"Successfully added make '%s'" % make.name, "success")
        except exc.SQLAlchemyError:
            flash(u"Make '%s' already exists in the database." % make.name, "warning")
        return redirect(url_for('admin.add_make'))
    return render_template('admin/add_make.html', form=form)


@mod.route('/admin/configuration/add_model/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_model():
    form = AddModelForm()
    form.make.choices = sorted([(x.id, x.name) for x in Make.query.all()], key=lambda x: x[1])
    if form.validate_on_submit():
        model = Model(
            make = Make.query.get(form.data['make']),
            name = form.data['name'],
            vintage = form.data['vintage'],
            notes = form.data['notes'])
        db.session.add(model)
        try:
            db.session.commit()
            flash(u"Successfully added model '%s'" % model.name, "success")
        except exc.SQLAlchemyError:
            flash(u"Model '%s' already exists in the database." % model.name, "warning")
        return redirect(url_for('admin.add_model'))
    return render_template('admin/add_model.html', form=form)


@mod.route('/admin/utilities/clean_database/')
@login_required
@admin_required
def clean_database():
    try:
        delete_count_users = User.query.filter_by(role=0).delete()
        delete_count_surveys = Survey.query.delete()
        db.session.commit()
    except:
        db.session.rollback()
    flash(u"Successfully cleaned the database.  Deleted '%s' non-admin users and '%s' surveys." % (delete_count_users, delete_count_surveys), "info")
    return redirect(url_for('admin.admin'))


@mod.route('/admin/utilities/clear_database/')
@login_required
@admin_required
def clear_database():
    try:
        User.query.filter_by(role=0).delete()
        Survey.query.delete()
        Model.query.delete()
        Make.query.delete()
        db.session.commit()
    except:
        db.session.rollback()
    flash(u"Successfully cleared the database.  Deleted all non-admin users, makes, models, and surveys.", "info")
    return redirect(url_for('admin.admin'))
