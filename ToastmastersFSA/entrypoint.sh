#!/bin/bash

set -e

if [ "$1" != "celery" ]; then
    python manage.py migrate
fi

if [ "$1" = "gunicorn" ]; then
    exec gunicorn ToastmastersFSA.wsgi:application --bind 0.0.0.0:8000
elif [ "$1" = "celery" ]; then
    cd /app
    exec celery -A ToastmastersFSA.celery worker --loglevel=info
elif [ "$1" = "test" ]; then
    python manage.py test
else
    exec python manage.py runserver 0.0.0.0:8000
fi