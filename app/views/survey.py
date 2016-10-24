# -*- coding: utf-8 -*-

from flask import render_template, redirect
from flask import url_for, g, request, session
from flask.ext.login import current_user, login_required

from app import app, db
from app.models import Survey, Beer
from app.forms import SurveyForm


@app.route('/survey/', methods=['GET', 'POST'])
@login_required
def survey():
    beer_id = request.args.get('beer_id', None)
    if beer_id:
        session['beer_id'] = beer_id
    form = SurveyForm(request.form)
    if request.method == 'POST' and form.validate():
        survey = Survey()
        form.populate_obj(survey)
        survey.user = current_user
        survey.beer = Beer.query.get(session['beer_id'])
        db.session.add(survey)
        db.session.commit()
        return redirect(request.args.get("next") or url_for("index"))
    return render_template('survey/survey.html', title='Survey', form=form)
