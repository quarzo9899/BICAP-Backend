#!/bin/bash

NAME="DjangoBICAP"
DJANGODIR=/home/django/DjangoBICAP
SOCKFILE=/home/django/django_env/run/gunicorn.sock
USER=django
GROUP=django
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=DjangoBICAP.settings
DJANGO_WSGI_MODULE=DjangoBICAP.wsgi
echo "Starting $NAME as whoami"


cd $DJANGODIR
source /home/django/django_env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \