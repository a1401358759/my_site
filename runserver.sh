#!/usr/bin/env bash
BASE_DIR=`dirname $0`
WORK_DIR=`pwd`/$BASE_DIR
LOG_DIR=$BASE_DIR/log
GUNICORN_PID_FILE=`pwd`/$LOG_DIR/gunicorn.pid
SCRIPT_NAME=runserver.sh
PYTHON_PATH=`which python`
INI_FILE=$WORK_DIR/gunicorn.conf

start_web() {
    echo Start Gunicorn Server
    gunicorn -c $INI_FILE my_site.wsgi:application
}

stop_web() {
	if [ -f $GUNICORN_PID_FILE ]; then
		echo Stop Gunicorn Server
		for pid in `cat $GUNICORN_PID_FILE`
		do
            kill $pid
        done
		rm -f $GUNICORN_PID_FILE
	fi
}

reload_web() {
    if [ -f $GUNICORN_PID_FILE ]; then
        echo Reload Gunicorn Server
        kill -HUP `cat $GUNICORN_PID_FILE`
    else
        start_web
    fi
}

case $1 in
    start-web):
        start_web
        ;;
    stop-web)
        stop_web
        ;;
    restart-web)
        reload_web
        ;;
    *)
        echo "Usage: $SCRIPT_NAME (
            start-web|stop-web|restart-web
            )"
        ;;
esac
