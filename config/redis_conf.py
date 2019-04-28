# -*- coding: utf-8 -*-

from redis.sentinel import Sentinel


class RedisClient(object):
    sentinel = Sentinel([
        ('127.0.0.1', 26379),
        ('127.0.0.1', 26380),
    ])
    TIMEOUT = 0.5
    user_db = sentinel.master_for("mymaster", socket_timeout=TIMEOUT, db=0)
