from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import SubmitField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired


csrf = CSRFProtect()


class LoginForm(FlaskForm):
    name = StringField(u'Name', validators=[DataRequired()])
    submit = SubmitField(u"Sign in")


class SurveyForm(FlaskForm):
    rating = SelectField(u'Rating',
        choices=[('1', u'One point'), ('2', u'Two points'),
            ('3', u'Three points'), ('4', u'Four points'), ('5', u'Five points')],
        validators=[DataRequired()], default=None)
    submit = SubmitField(u"Submit")


class AddBrandForm(FlaskForm):
    name = StringField(u"Brand", validators=[DataRequired()], default=None)
    submit = SubmitField(u"Submit")


class AddModelForm(FlaskForm):
    brand = SelectField(u"Brand", validators=[DataRequired()], coerce=int)
    name = StringField(u"Model", validators=[DataRequired()])
    notes = TextAreaField(u"Notes")
    submit = SubmitField(u"Submit")
