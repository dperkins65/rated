#
# This setup script cleans and builds the link-generator package
#

import os, sys
from setuptools import setup, Command


class CleanAll(Command):
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -vr ./build ./dist ./*.pyc ./*.egg-info')


class CleanSome(Command):
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -vr ./build ./*.egg-info')


setup(
    name='rated',
    version='1.0.0',
    packages=['app'],
    package_data={
        'app': [
            'views/*',
            'templates/*',
            'templates/admin/*',
            'static/js/*',
            'static/css/*',
            'static/img/*'
        ],
    },
    exclude_package_data={
        '': [
            '*.pyc',
            '__pycache__',
            '.DS_Store',
        ],
    },
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_wtf',
        'flask_login',
        'PyMySQL',
        'pytest',
        'numpy',
    ],
    cmdclass={
        'clean_pre_build': CleanAll,
        'clean_post_build': CleanSome,
    }
)
