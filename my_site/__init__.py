from __future__ import absolute_import

# 使用PyMySQL连接数据库时需要打开下面两条注释， 目前使用mysqlclient连接数据库
# import pymysql
# pymysql.install_as_MySQLdb(MySQLdb_version=(1, 4, 2, "final", 0))

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app
__all__ = ['celery_app']
