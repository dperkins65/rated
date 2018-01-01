import sys
from os import environ
from flask import Flask, render_template

from app.config import Config, DevelopmentConfig, UnitTestConfig, TestingConfig
from app.views import index, user, admin, survey
from app.views.user import lm
from app.database import db
from app.commands import create_db, drop_db, populate_db, recreate_db
from app.forms import csrf


def create_app(default_config='Config'):
    """Returns an initialized Flask application."""
    app = Flask(__name__)

    #
    # Set the configuration. This defaults to default_config if the env var
    # FLASK_CONFIG is not set. If it is set then it loads one of the other
    # configurations from app.config as long as it has been imported into this module.
    #
    config = environ.get('FLASK_CONFIG', default_config)
    app.config.from_object(getattr(sys.modules[__name__], config))
    app.logger.debug("Using configuration '%s'" % config)

    #
    # Register application components
    #
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_commands(app)
    app.logger.debug("Application component registration completed")

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    db.init_app(app)
    csrf.init_app(app)
    lm.init_app(app)


def register_blueprints(app):
    """Register blueprints with the Flask application."""
    app.register_blueprint(index.mod)
    app.register_blueprint(user.mod)
    app.register_blueprint(admin.mod)
    app.register_blueprint(survey.mod)


def register_errorhandlers(app):
    """Register error handlers with the Flask application."""

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error(e)
        return render_template('404.html', error=str(e)), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(e)
        return render_template('500.html', error=str(e)), 500

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        app.logger.error(e)
        return render_template('500.html', error=str(e)), 500


def register_commands(app):
    """Register custom commands for the Flask CLI."""
    for command in [create_db, drop_db, populate_db, recreate_db]:
        app.cli.command()(command)

#
# Instantiate the application
#
app = create_app()
