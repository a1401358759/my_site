# -*- coding: utf-8 -*-

from functools import wraps
from fnmatch import fnmatch

from django.http import HttpResponseForbidden
from utils.dlibs.tools.tools import get_clientip


def restrict_white_ip_access(config):
    """view IP校验装饰器

    :param config: 白名单配置项，格式：
                    {
                        'domain': ['127.0.0.1', '10.*.*.*'],
                        'description': u'示例'
                    }
    """

    def decorator(view_func):
        @wraps(view_func)
        def _validate_access(request, *args, **kwargs):
            allowed_ips = config.get('domain') or []
            # 验证IP
            ip_permission = False
            client_ip = get_clientip(request)
            if len(allowed_ips) == 0 or allowed_ips[0] == '*':
                ip_permission = True
            else:
                for ip in set(allowed_ips):
                    if fnmatch(client_ip, ip):
                        ip_permission = True
                        break
            if not ip_permission:
                return HttpResponseForbidden("REQUEST IP %s IS NOT ALLOWED" % client_ip)

            response = view_func(request, *args, **kwargs)
            return response

        return _validate_access

    return decorator
