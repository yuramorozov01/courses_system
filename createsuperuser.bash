#!/bin/bash

docker-compose exec courses python3 ./src/manage.py createsuperuser
