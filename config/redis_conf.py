# -*- coding: utf-8 -*-
from redis.sentinel import Sentinel


class RedisClient(object):
    sentinel = Sentinel([
        ('sentinel.zhengyi.dev', 26379),
        ('sentinel.zhengyi.dev', 26380),
    ])
    TIMEOUT = 0.5
    activity_conf_db = sentinel.master_for("mymaster", socket_timeout=TIMEOUT, db=0)
    activity_db = sentinel.master_for("mymaster", socket_timeout=TIMEOUT, db=0)
    company_info_db = sentinel.master_for("mymaster", socket_timeout=TIMEOUT, db=1)
    user_info_db = sentinel.master_for("mymaster", socket_timeout=TIMEOUT, db=2)
    captcha_limit_db = sentinel.master_for("mymaster", socket_timeout=TIMEOUT, db=5)
    member_db = sentinel.master_for("mymaster", socket_timeout=TIMEOUT, db=6)
