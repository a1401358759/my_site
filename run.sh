#!/bin/bash

python3 manage.py migrate&&
supervisord -n -c supervisor.conf
