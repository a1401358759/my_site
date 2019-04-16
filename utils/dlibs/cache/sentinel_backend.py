#!/usr/bin/env python
# -*- coding: utf-8  -*-
from redis_backend import RedisCache, CacheClass, ImproperlyConfigured
from redis.sentinel import Sentinel, SentinelConnectionPool


class SentinelRedisCache(RedisCache):

    """
    支持sentinel机制的哨兵redis client
    """

    def _init(self, server, params):
        super(CacheClass, self).__init__(params)
        self._server = server
        self._params = params

        self.service_name = self.options.get("SERVICE_NAME", 'mymaster')
        self.slave_read = self.options.get("READ_SLAVE", False)
        if self.server:
            def _get_hosttupe(conn):
                host_lst = conn.rsplit(':', 1)
                return host_lst[0], int(host_lst[1])

            conn_list = [_get_hosttupe(conn) for conn in self.server]

        else:
            raise ImproperlyConfigured("sentinel server config error.")

        kwargs = self.connection_pool_class_kwargs
        max_connections = kwargs.pop('max_connections')
        sentinel_manager = Sentinel(conn_list, sentinel_kwargs=kwargs)

        kwargs.update({
            'db': self.db,
            'password': self.password,
            'max_connections': max_connections
        })
        self._client = sentinel_manager.master_for(self.service_name,
                                                   connection_pool_class=self.connection_pool_class,
                                                   **kwargs)

        if self.slave_read:
            self._slave_client = sentinel_manager.slave_for(self.service_name,
                                                            connection_pool_class=self.connection_pool_class,
                                                            **kwargs)

    @property
    def server(self):
        return self._server or ["127.0.0.1:6379"]

    @property
    def slave_client(self):
        if not self.slave_read:
            return self._client

        return self._slave_client

    @property
    def connection_pool_class(self):
        return SentinelConnectionPool

    def ping(self):
        self.client.ping()
        if self.slave_read:
            self.slave_client.ping()

    def _mget(self, keys):
        if self.slave_read:
            results = self.slave_client.mget(keys)
        else:
            results = self.client.mget(keys)
        return results

    def _get(self, key):
        if self.slave_read:
            value = self.slave_client.get(key)
        else:
            value = self.client.get(key)

        return value

    def has_key(self, key, version=None):
        """
        Returns True if the key is in the cache and has not expired.
        """
        key = self.make_key(key, version=version)
        if self.slave_read:
            return self.slave_client.exists(key)
        else:
            return self.client.exists(key)
