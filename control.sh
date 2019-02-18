#!/bin/sh

RED_COLOR='\E[1;31m' #红
YELOW_COLOR='\E[1;33m' #黄
BLUE_COLOR='\E[1;34m'  #蓝
RES='\E[0m'

# 启动uwsgi服务
if [ "$1" == "start_uwsgi" ]; then
    uwsgi -i etc/uwsgi.ini &
    exit
fi

# 重启uwsgi服务
if [ "$1" == "restart_uwsgi" ]; then
    uwsgi --reload /var/run/uwsgi/project.pid
    exit
fi

# 更新代码，更新pip依赖，重启uwsgi服务
if [ "$1" == "update_restart_uwsgi" ]; then
    git pull
    pip install -r requirements.txt | grep -v "Requirement already satisfied"
    uwsgi --reload /var/run/uwsgi/project.pid
    exit
fi

# 直接执行传入的命令
if [ "$1" == "eval" ]; then
    if [ $# != 2 ] ; then
        printf "${RED_COLOR}eval后只支持一个参数，如果命令由多个词组成请使用''括起来${RES}\n"
    else
        source /opt/django/venv/bin/activate
        eval $2
    fi
    exit
fi

printf "参数:\n"
printf "${BLUE_COLOR}start_uwsgi${RES}               ${YELOW_COLOR}启动uwsgi服务${RES}\n"
printf "${BLUE_COLOR}restart_uwsgi${RES}             ${YELOW_COLOR}重启uwsgi服务${RES}\n"
printf "${BLUE_COLOR}update_restart_uwsgi${RES}      ${YELOW_COLOR}更新代码，更新pip依赖，重启uwsgi服务${RES}\n"
printf "${BLUE_COLOR}eval 'some shell cmd'${RES}     ${YELOW_COLOR}直接执行传入的命令${RES}\n"
