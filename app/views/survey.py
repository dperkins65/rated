# -*- coding: utf-8 -*-

from flask import render_template, redirect
from flask import url_for, g, request
from flask.ext.login import current_user, login_required

from app import app, db
from app.models import User, Survey1
from app.forms import Survey1Form


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
