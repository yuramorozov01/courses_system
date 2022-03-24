#!/bin/bash

cd src
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
daphne -b 0.0.0.0 -p 8000 courses.asgi:application
