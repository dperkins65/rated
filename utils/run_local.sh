#!/bin/bash
#
# Shorcut for running the app via Flask CLI
#
# This is the primary method for running the app during development.
# First installs the local package with pip3 in dev mode and then
# runs the application with the dev config.
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pip3 install -e $DIR/../

export FLASK_APP=app

flask recreate_db
flask run
