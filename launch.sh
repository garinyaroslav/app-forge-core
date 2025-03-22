#!/usr/bin/env bash

source "./bin/activate"
docker-compose up -d
python core/manage.py runserver

