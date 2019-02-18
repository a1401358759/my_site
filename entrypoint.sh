#!/bin/sh
set -e

# create and use virtualenv
VENV_DIR="/home/data/venv/my_site"
VENV_ACTIVATE_PATH="/home/data/venv/my_site/bin/activate"
if [ ! -d "$VENV_ACTIVATE_PATH" ]; then
  virtualenv $VENV_DIR
fi
source $VENV_ACTIVATE_PATH

exec "$@"
