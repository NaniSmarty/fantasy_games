#!/bin/bash
# Name of the application
NAME="fantasy_game"

# Django project directory
DJANGODIR=/home/narayanaraju/fantasy_game/fantasygame

# we will communicte using this unix socket
SOCKFILE=/home/narayanaraju/fantasy_game/fantasygame/run/gunicorn.sock

# the user to run as
USER=narayanaraju

# the group to run as
GROUP=narayanaraju

# how many worker processes should Gunicorn spawn
NUM_WORKERS=9

# how many number of threads each worker should have
NUM_THREADS=20

# which settings file should Django use
DJANGO_SETTINGS_MODULE=fantasygame.settings

# WSGI module name
DJANGO_WSGI_MODULE=fantasygame.wsgi

# Activate the virtual environment
cd $DJANGODIR
source /home/narayanaraju/fantasy_game/venv/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/narayanaraju/fantasy_game/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--threads $NUM_THREADS \
--user=$USER --group=$GROUP \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=-







