#!/bin/sh

# install uwsgi and requirements
pip install uwsgi==2.0.12
pip install -r requirement.txt

# TODO git pull

# runserver
uwsgi -i etc/uwsgi.ini
