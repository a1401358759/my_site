#!/bin/bash

# install uwsgi and requirements
pip install uwsgi==2.0.12
pip install -r requirement.txt

# TODO git pull

# runserver
../venv/bin/uwsgi -i etc/uwsgi.ini
