#!/bin/bash

pip install uwsgi==2.0.12
pip install -r requirement.txt
./manage.py migrate --noinput

# TODO git pull

# runserver
uwsgi -i etc/uwsgi.ini
