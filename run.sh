#!/bin/bash

# Pass 'x' as a command line argument to enable external IPs
opts=$1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $DIR/../bin/activate
rm $DIR/../*.db
python $DIR/manage.py initdb

if [ "$opts" = "x" ]; then
  # External debug
  echo 'Current server address:'
  ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'
  python $DIR/manage.py runserver -h 0.0.0.0 -p 5000 -r -d
else
  # Normal debug
  python $DIR/manage.py runserver -r -d
fi
