# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import Celery, platforms

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_site.settings')

# from django.conf import settings

platforms.C_FORCE_ROOT = True   # 允许用root用户启动celery

app = Celery('my_site')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
