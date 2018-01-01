#
# This runner script helps uwsgi instantiate the app because it cannot
# call the Python package directly (i.e. call __init__.py).
#
# Note, the import here works becasue the app is packaged using setuptools
# and then installed into the target host/container.  The package 'app'
# is inherently in the PYTHONPATH.  See ../app/__init__.py for details.
#

from app import app

if __name__ == "__main__":
    app.run()
