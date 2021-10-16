import multiprocessing

bind = '0.0.0.0:9000'  # 绑定ip和端口号
workers = multiprocessing.cpu_count() * 2 + 1  # 进程数
worker_class = "gevent"
worker_connections = 2048
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置
accesslog = "logs/gunicorn_access.log"  # 访问日志文件
errorlog = "logs/gunicorn_error.log"  # 错误日志文件
pidfile = "logs/gunicorn.pid"
timeout = 300  # 5分钟超时，上传文件超时问题
backlog = 10240
limit_request_fields = 32768  # 最大值32768, 头的key个数
limit_request_field_size = 0  # 头大小，0为不限
