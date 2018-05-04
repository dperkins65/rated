from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import SubmitField, SelectField, StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, Optional


csrf = CSRFProtect()


class LoginForm(FlaskForm):
    name = StringField(u'Name', validators=[DataRequired()])
    submit = SubmitField(u"Sign in")


class SurveyForm(FlaskForm):
    rating = SelectField(u'Rating',
        choices=[('1', u'One point'), ('2', u'Two points'),
            ('3', u'Three points'), ('4', u'Four points'), ('5', u'Five points')],
        validators=[DataRequired()], default=None)
    notes = TextAreaField(u"Notes")
    submit = SubmitField(u"Submit")


class AddMakeForm(FlaskForm):
    name = StringField(u"Make", validators=[DataRequired()])
    submit = SubmitField(u"Submit")


class AddModelForm(FlaskForm):
    name = StringField(u"Model", validators=[DataRequired()])
    make = SelectField(u"Make", validators=[DataRequired()], coerce=int)
    vintage = DateField(u"Vintage", validators=[Optional()])
    notes = TextAreaField(u"Notes")
    submit = SubmitField(u"Submit")
