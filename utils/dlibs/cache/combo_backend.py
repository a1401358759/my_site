#!/usr/bin/env python
# -*- coding: utf-8  -*-
try:
    from django.utils.six.moves import cPickle as pickle
except ImportError:
    import pickle
from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from django.core.cache.backends.locmem import dummy
from utils.libs.logger.syslogger import SysLogger
from utils.dlibs.tools.tools import get_cache


class ComboCache(BaseCache):
    """
    多级复合缓存:
        remote cache（默认） -- 远端集中缓存
        local cache  -- 本地内存缓存,目前只是支持django.core.cache.backends.locmem.LocMemCache
    eg：

        # 复合缓存配置
        'combo-local': {
            'BACKEND': 'libs.djangos.cache.combo_backend.ComboCache',
            'REMOTE_CACHE':'cache-alias', # 复合缓存使用的远端缓存alias name
            'LOCAL_CACHE': 'cache-alias',# 复合缓存使用的local缓存alias name
        },
    """
    def __init__(self, server, params):
        super(ComboCache, self).__init__(params)
        self.localc = get_cache(params.get('LOCAL_CACHE'))  # local cache
        self.remotec = get_cache(params.get('REMOTE_CACHE'))

    def _printexc(self, ex):
        SysLogger.exception(ex)

    def get(self, key, default=None, version=None, acquire_lock=True, timeout_local=DEFAULT_TIMEOUT):
        """
        get value. get --> local --> remote.

        If get remote failed, reuse local value.

        :param key: key
        :param default: 如果local和remote都为None，返回default
        :param version: version
        :param timeout_local: 默认本地的缓存过期时间
        :return:
        """
        make_key = self.localc.make_key(key, version=version)
        self.localc.validate_key(make_key)
        value = None
        with (self.localc._lock.reader() if acquire_lock else dummy()):
            pickled = self.localc._cache.get(make_key)
            expired = self.localc._has_expired(make_key)
        if pickled is not None:
            try:
                value = pickle.loads(pickled)
            except pickle.PickleError:
                value = None

        if (expired is False) and (value is not None):
            return value
        elif expired:
            self.localc.delete(key, version=version)

        # local数据异常，查remote cache
        try:
            # 尝试从remote cache 读取
            remote_value = self.remotec.get(key=key, version=version)
        except Exception, ex:
            # 如果backend cache异常，且cache值不为None，则local重新缓存这个key，
            # 并且延长timeout_local设定的时间, 下次会直接命中local
            self._printexc(ex)
            if value is not None:
                self.localc.set(key, value, timeout=timeout_local, version=version)
        else:
            # 如果remote cache未异常，更新local cache
            if (remote_value is not None) or self.remotec.has_key(key, version=version):
                self.localc.set(key, remote_value, timeout=timeout_local, version=version)
                value = remote_value
        return value or default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None, timeout_local=DEFAULT_TIMEOUT):
        '''同时设置local、remote cache'''
        # 1. set local
        self.localc.set(key, value, timeout_local, version)
        # 2. set remote
        try:
            self.remotec.set(key, value, timeout, version)
        except Exception, ex:
            self._printexc(ex)
