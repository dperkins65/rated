import os
from datetime import timedelta


APPLICATION_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(APPLICATION_ROOT)


class Config(object):
    """This base config also serves as the default/production config"""
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    SECRET_KEY = 'ax8a4xbM<LbxfqDl8$xd8ex81pxE99Fxcvx19@Dx9A::1kjdfkj*aEx8fY'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_QUERY_TIMEOUT = 15

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=240)


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False


class UnitTestConfig(Config):
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
