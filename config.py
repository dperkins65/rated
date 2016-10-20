# -*- coding: utf-8 -*-

import os

PROJECT = 'rated'

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TESTING = False

SECRET_KEY = 'N2aKFXXaXger6r78Hw'

SQLALCHEMY_ECHO = True
DATABASE_QUERY_TIMEOUT = 15
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/%s.db' % PROJECT
