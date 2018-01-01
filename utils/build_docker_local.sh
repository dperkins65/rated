#!/bin/bash
#
# This script builds the application, containers, and runs them locally
#
# Note, if the containers are not cleaned up on exit, run 'docker-compose kill'
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR/../

# Build the app package
python setup.py clean_pre_build
python setup.py sdist
python setup.py clean_post_build

# The following approach rebuilds the containers every time.
# Remove --build to significantly speed things up.
docker rm rated_app_1
docker rm rated_proxy_1
docker-compose up --build --abort-on-container-exit --remove-orphans
