from flask import Blueprint, render_template, redirect
from flask import url_for, g, request, session, flash
from flask_login import current_user, login_required

from app.database import db, Survey, Model
from app.forms import SurveyForm


mod = Blueprint('survey', __name__)


@mod.route('/survey/', methods=['GET', 'POST'])
@login_required
def survey():
    g.user = current_user
    model_id = request.args.get('model_id', None)
    if model_id:
        session['model_id'] = model_id
    form = SurveyForm()
    if request.method == 'POST' and form.validate():
        survey = Survey()
        form.populate_obj(survey)
        survey.user = g.user
        survey.model = Model.query.get(session['model_id'])
        db.session.add(survey)
        db.session.commit()
        flash("Submission complete", "success")
        return redirect(url_for("index.index"))
    return render_template('survey.html', form=form)
