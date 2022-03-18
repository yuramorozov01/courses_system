#!/bin/bash

cd src
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn -b 0.0.0.0:8000 courses.wsgi
