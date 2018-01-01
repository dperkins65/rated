from flask import Blueprint, render_template, request, g, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from app.database import db, User
from app.forms import LoginForm


lm = LoginManager()
lm.login_view = 'user.login'
lm.login_message_category = "info"


mod = Blueprint('user', __name__)


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data.lower()
        try:
            user = User.query.filter_by(name=name).first()
            login_user(user)
        except: #TODO fix exception type/reason
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        user = g.user
        if current_user.is_admin:
            return redirect(url_for('admin.admin'))
        else:
            return redirect(url_for("index.index"))
    return render_template('login.html', form=form)


@mod.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@mod.before_app_request
def before_request():
    g.user = current_user
