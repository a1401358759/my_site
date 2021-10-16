#!/bin/bash

git pull&&
pip3 install -r requirements.txt&&
python3 manage.py migrate&&
supervisord -n -c supervisor.conf
