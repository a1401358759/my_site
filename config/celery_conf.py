# -*- coding: utf-8 -*-

from celery.schedules import crontab

CELERY_WORKER_MAX_TASKS_PER_CHILD = 100000  # 每个worker执行10w个任务就会被销毁，可防止内存泄露
CELERY_BROKER_URL = "redis://127.0.0.1:6379/3"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/4"
CELERY_RESULT_EXPIRES = 3600 * 24  # 任务多久被清除
CELERY_TASK_IGNORE_RESULT = False  # 一般不关注结果，请开启该设置，如果要存结果，请配置CELERY_RESULT_BACKEND
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_TASK_DEFAULT_EXCHANGE = 'mysite_exchange'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_QUEUE = 'mysite_queue'  # 默认是celery,一般修改
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'

# CELERY_BROKER_HEARTBEAT = 10  # 心跳
# crotab任务
CELERY_BEAT_SCHEDULE = {
    # 'refund_transfers': {
    #     'task': 'app.order.tasks.refund_transfers',
    #     'schedule': crontab(minute='0', hour='8'),
    # },
}

CELERY_SEND_TASK_ERROR_EMAILS = True  # 错误发送邮件
