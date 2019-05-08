# -*- coding: utf-8  -*-
from config.common_conf import AliyunOssProtectedConf
from utils.libs.utils.aliyunoss import AliyunOssApi

try:
    import cPickle as pickle
except ImportError:
    import pickle
import django


if django.VERSION >= (1, 7):  # pragma: nocover

    def get_cache(name):
        from django.core.cache import caches
        return caches[name]
else:
    from django.core.cache import get_cache  # pragma: nocover


class PickleSerializer(object):
    """ pickle serializer except int """
    def dumps(self, obj):
        if not isinstance(obj, int) or isinstance(obj, bool):
            return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
        else:
            return obj

    def loads(self, obj):
        try:
            value = int(obj)
        except (ValueError, TypeError):
            value = pickle.loads(obj)
        return value


def get_ip_address(request):
    """
    获取ip地址
    :param request:
    :return:
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")
    client_ip = ip.split(",")[-1].strip() if ip else ""
    return client_ip


def get_clientip(request, distinct=True):
    """
    获得客户端ip
    :param request:
    :return: clientip or ''
    """
    serverip = request.META.get("HTTP_NS_CLIENT_IP")  # NAT模式新加的header
    if not serverip or serverip.lower() == 'unknown':
        serverip = request.META.get('HTTP_X_FORWARDED_FOR') or ''
    if not serverip or serverip.lower() == 'unknown':
        serverip = request.META.get('HTTP_PROXY_CLIENT_IP') or ''
    if not serverip or serverip.lower() == "unknown":
        serverip = request.META.get('HTTP_WL_PROXY_CLIENT_IP') or ''
    if not serverip or serverip.lower() == 'unknown':
        serverip = request.META.get('REMOTE_ADDR') or ''
    if serverip and serverip.lower() != "unknown":
        if distinct:
            serverip_list = []
            for ip in serverip.split(','):
                ip = ip.strip()
                if ip and ip not in serverip_list:
                    serverip_list.append(ip)
            serverip = ','.join(serverip_list)
        return serverip
    return ''


class OSSTool(object):
    '''
    之后转到libs中
    '''
    oss_protect_client = AliyunOssApi(**AliyunOssProtectedConf)

    @classmethod
    def sign_protect_url(cls, filename):
        return cls.oss_protect_client.make_url(filename)
