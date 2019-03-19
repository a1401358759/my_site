# -*- coding: utf-8  -*-
'''
请求初始化预处理：
    1. GET、POST参数整合到parameters
'''
import django
from django.http import HttpResponseBadRequest, QueryDict

from utils.dlibs.tools.tools import get_clientip
from utils.libs.logger import SysLogger

if django.VERSION[:3] >= (1, 10, 0):
    # 新版本中,middle需要继承这个类
    from django.utils.deprecation import MiddlewareMixin
    BaseMiddleCls = MiddlewareMixin
else:
    BaseMiddleCls = object


class RequestInfo(object):
    DATA = {}


class RequestInitMiddleware(BaseMiddleCls):
    '''请求初始化预处理'''
    def process_request(self, request):
        try:
            # 1. GET参数整合到parameters
            request.parameters = request.GET.copy()
            if request.method == "POST":
                # 2. 处理request.body内的query_string更新到request.parameters
                # multipart/form-data 时不处理表单里的参数，因为没有经过nginx的参数签名校验，无法保证参数合法性
                if request.META['CONTENT_TYPE'].startswith('multipart/form-data'):
                    return None
                # application/x-www-form-urlencoded 时不处理request.body
                elif request.META['CONTENT_TYPE'] == 'application/x-www-form-urlencoded':
                    pass
                # xml or json 时不处理request.body
                elif request.body.startswith("<") or request.body.startswith("{") or request.body.startswith("["):
                    pass
                # 其他情况更新request.body内的query_string到request.parameters
                elif '=' in request.body:
                    request.parameters.update(QueryDict(request.body, encoding='utf-8'))

                # 3. 表单参数更新到request.parameters
                for k in request.POST:
                    # 使用setlist以支持类似复选控件一个name多个value的情况
                    request.parameters.setlist(k, request.POST.getlist(k))
            # 提取用户的客户端信息
            RequestInfo.DATA = {
                "request_ip": get_clientip(request),
                "user_agent": request.META.get("HTTP_USER_AGENT", "")
            }
            # 安全日志部分到此为止
            return None
        except Exception as ex:
            SysLogger.exception(ex, request)
            response = HttpResponseBadRequest()
            return response
