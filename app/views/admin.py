from __future__ import division

import numpy, sys, json
from operator import itemgetter

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required

from sqlalchemy import func, exc, desc

from app.database import db, User, Survey, Model, Brand
from app.decorators import admin_required
from app.forms import AddModelForm, AddBrandForm


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


@mod.route('/admin/results/')
@login_required
@admin_required
def results():
    models = Model.query.all()
    surveys = Survey.query.all()
    results = []
    for model in models:
        ratings_list = [survey.rating for survey in surveys if survey.model == model]
        if not ratings_list:
            ratings_list = [0]
        ratings_array = numpy.array(ratings_list)
        ratings_mean = numpy.nan_to_num(numpy.around(numpy.mean(ratings_array, axis=0), decimals=2))
        ratings_std = numpy.nan_to_num(numpy.around(numpy.std(ratings_array, axis=0), decimals=2))
        try:
            ratings_range = (min(ratings_list), max(ratings_list))
        except ValueError:
            ratings_range = (int(0), int(0))
        user_ratings = [{'user': survey.user.name,
                         'rating': survey.rating} for survey in surveys if survey.model == model]
        results.append({'model_id': model.id,
                        'model_name': model.name,
                        'model_notes': model.notes,
                        'brand_name': model.brand.name,
                        'ratings_mean': ratings_mean,
                        'ratings_std': ratings_std,
                        'ratings_range': ratings_range,
                        'user_ratings': user_ratings,
                        })
    results = sorted(results, key=itemgetter('ratings_mean'))
    return render_template('admin/results.html', results=results)


@mod.route('/admin/result/<int:model_id>')
@login_required
@admin_required
def result(model_id):
    surveys = Survey.query.filter_by(model_id=model_id).order_by(desc('rating'))
    return render_template('admin/result.html', surveys=surveys)


@mod.route('/admin/configuration/')
@login_required
@admin_required
def configuration():
    models = Model.query.all()
    return render_template('admin/configuration.html', models=models)


@mod.route('/admin/configuration/add_brand/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_brand():
    form = AddBrandForm()
    if form.validate_on_submit():
        brand = Brand()
        form.populate_obj(brand)
        db.session.add(brand)
        try:
            db.session.commit()
            flash(u"Successfully added brand '%s'" % brand.name, "success")
        except exc.SQLAlchemyError:
            flash(u"Brand '%s' already exists in the database." % brand.name, "warning")
        return redirect(url_for('admin.add_brand'))
    return render_template('admin/add_brand.html', form=form)


@mod.route('/admin/configuration/add_model/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_model():
    form = AddModelForm()
    form.brand.choices = sorted([(x.id, x.name) for x in Brand.query.all()], key=lambda x: x[1])
    if form.validate_on_submit():
        model = Model(
            brand = Brand.query.get(form.data['brand']),
            name = form.data['name'],
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
        Brand.query.delete()
        db.session.commit()
    except:
        db.session.rollback()
    flash(u"Successfully cleared the database.  Deleted all non-admin users, brands, models, and surveys.", "info")
    return redirect(url_for('admin.admin'))
