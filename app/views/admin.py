# -*- coding: utf-8 -*-

from __future__ import division

import numpy, sys, json
from operator import itemgetter

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required

from sqlalchemy import func, exc

from app import app, db
from app.decorators import admin_required
from app.models import User, Survey, Beer, Brewery, Style
from app.forms import AddBeerForm, AddBreweryForm, AddStyleForm


@app.route('/admin/index')
@login_required
@admin_required
def admin():
    users = User.query.filter_by(role=0)
    all_beers = Beer.query.all()
    return render_template('admin/index.html', title="Admin", users=users, all_beers=all_beers)


@app.route('/admin/survey/')
@login_required
@admin_required
def admin_survey():
    beer_id = request.args.get('beer_id', None)
    surveys = Survey.query.filter_by(beer_id=beer_id)
    survey_count = surveys.count()
    user_count = User.query.filter_by(role=0).count()
    try:
        percent_complete = (survey_count / user_count * 100)
    except ZeroDivisionError:
        percent_complete = float('Inf')
    ratings_array = numpy.array([survey.rating for survey in surveys])
    ratings_mean = numpy.mean(ratings_array, axis=0)
    ratings_stdev = numpy.std(ratings_array, axis=0)
    return render_template('admin/survey.html',
                           title='Admin Beer %s' % beer_id,
                           beer_id=beer_id,
                           surveys=surveys,
                           percent_complete=percent_complete,
                           ratings_mean=ratings_mean,
                           ratings_stdev=ratings_stdev)


@app.route('/admin/results_review')
@login_required
@admin_required
def results_review():
    beers = Beer.query.all()
    surveys = Survey.query.all()
    data = []
    for beer in beers:
        ratings_list = [survey.rating for survey in surveys if survey.beer == beer]
        ratings_array = numpy.array(ratings_list)
        ratings_mean = numpy.nan_to_num(numpy.around(numpy.mean(ratings_array, axis=0), decimals=2))
        ratings_stdev = numpy.nan_to_num(numpy.around(numpy.std(ratings_array, axis=0), decimals=2))
        try:
            ratings_range = (min(ratings_list), max(ratings_list))
        except ValueError:
            ratings_range = (int(0), int(0))
        user_ratings = [{'user': survey.user.name,
                         'rating': survey.rating} for survey in surveys if survey.beer == beer]
        data.append({'beer_id': beer.id,
                     'beer_name': beer.name,
                     'brewery_name': beer.brewery.name,
                     'ratings_mean': ratings_mean,
                     'ratings_stdev': ratings_stdev,
                     'ratings_range': ratings_range,
                     'user_ratings': user_ratings,
                     })
    sdata = sorted(data, key=itemgetter('ratings_mean'))
    jdata = json.dumps(data, sort_keys=False)
    return render_template('admin/review.html',
                           title='Results Review',
                           data=sdata,
                           jdata=jdata)


@app.route('/admin/ranking_overall')
@login_required
@admin_required
def ranking_overall():
    return render_template('admin/ranking.html', title='Overall Ranking')


@app.route('/admin/ranking_style')
@login_required
@admin_required
def ranking_style():
    return render_template('admin/ranking.html', title='Ranking by Style')


@app.route('/admin/ranking_ba')
@login_required
@admin_required
def ranking_ba():
    return render_template('admin/ranking.html', title='Ranking vs. BA Rating')


@app.route('/admin/add_style/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_style():
    form = AddStyleForm(request.form)
    if request.method == 'POST' and form.validate():
        style = Style()
        form.populate_obj(style)
        db.session.add(style)
        try:
            db.session.commit()
            flash(u"Successfully added style '%s'" % style.name)
        except exc.SQLAlchemyError:
            flash(u"Style '%s' already exists in the database." % style.name)
        return redirect(url_for('add_style'))
    return render_template('admin/add_style.html', title='Style Configuration', form=form)


@app.route('/admin/add_brewery/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_brewery():
    form = AddBreweryForm(request.form)
    if request.method == 'POST' and form.validate():
        brewery = Brewery()
        form.populate_obj(brewery)
        db.session.add(brewery)
        try:
            db.session.commit()
            flash(u"Successfully added brewery '%s'" % brewery.name)
        except exc.SQLAlchemyError:
            flash(u"Brewery '%s' already exists in the database." % brewery.name)
        return redirect(url_for('add_brewery'))
    return render_template('admin/add_brewery.html', title='Brewery Configuration', form=form)


@app.route('/admin/add_beer/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_beer():
    form = AddBeerForm(request.form)
    form.brewery.choices = sorted([(x.id, x.name) for x in Brewery.query.all()], key=lambda x: x[1])
    form.style.choices = sorted([(x.id, x.name) for x in Style.query.all()], key=lambda x: x[1])
    if request.method == 'POST' and form.validate():
        beer = Beer(
            brewery = Brewery.query.get(form.data['brewery']),
            name = form.data['name'],
            style = Style.query.get(form.data['style']),
            abv = form.data['abv'],
            ba = form.data['ba'],
            notes = form.data['notes'])
        db.session.add(beer)
        try:
            db.session.commit()
            flash(u"Successfully added beer '%s'" % beer.name)
        except exc.SQLAlchemyError:
            flash(u"Beer '%s' already exists in the database." % beer.name)
        return redirect(url_for('add_beer'))
    return render_template('admin/add_beer.html', title='Beer Configuration', form=form)
