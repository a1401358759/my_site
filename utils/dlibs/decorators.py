# -*- coding: utf-8  -*-
'''各种通用装饰器'''
import json
from functools import wraps

from django.http import HttpResponseNotAllowed

from utils.libs.error import CommonError, APIError
from .http import http_response
from utils.libs.logger import SysLogger


def request_checker(allow_anonymous=False, method="GET"):
    """请求校验装饰器，检查是否满足登录需求，检查请求method是否符合；同时支持捕获APIError异常转化为响应

    这个装饰器最好作为最后被执行的装饰器(最靠近view函数)，可以作为最后一道屏障捕获接口未捕获异常并返回UNKNOWN错误码

    allow_anonymous  -- 是否允许匿名访问
    method  -- 允许的http method, 为None表示不限制method
    """

    def decorator(view_func):
        @wraps(view_func)
        def _check_request(request, *args, **kwargs):
            if method and (request.method != method.upper()):
                return HttpResponseNotAllowed([method.upper()])
            statuscode = CommonError.UNKNOWN
            try:
                if allow_anonymous:
                    return view_func(request, *args, **kwargs)
                elif not request.user.is_authenticated():
                    statuscode = CommonError.NOT_LOGIN
                elif not request.user.is_active:
                    statuscode = CommonError.USER_DEACTIVE
                else:
                    return view_func(request, *args, **kwargs)
            except APIError as ex:
                statuscode = ex.statuscode
            except Exception as ex:
                SysLogger.exception(ex, request)
                statuscode = APIError().statuscode
            return http_response(request, statuscode=statuscode)

        return _check_request

    return decorator


def form_validator(form_class):
    '''Django Form表单校验装饰器，检查失败直接返回错误码PARAM_ERROR

    :form_class: - Form class
    '''
    def decorator(view_func):
        @wraps(view_func)
        def _validate_form(request, *args, **kwargs):
            form = None
            if request.method == 'GET':
                form = form_class(request.GET)
            elif request.method == 'POST':
                form = form_class(request.POST)
            if form is None:
                return view_func(request, *args, **kwargs)

            setattr(request, 'form', form)
            if not form.is_valid():
                return http_response(request, statuscode=CommonError.PARAM_ERROR, msg=form.errors)
            return view_func(request, *args, **kwargs)
        return _validate_form
    return decorator


def record_operate(model=None, action=""):
    """
    操作记录装饰器, 用于记录用户操作的装饰器
    """

    def decorator(view_func):
        @wraps(view_func)
        def _operate_record(request, *args, **kwargs):
            if request.method == "POST":
                data = json.dumps(request.POST).decode("raw_unicode_escape")
                try:
                    model.objects.create(
                        name=request.hera_user.user_name,
                        action=action,
                        user_id=request.hera_user.user_id,
                        data=data,
                    )
                except Exception as ex:
                    SysLogger.exception(ex, request)
            return view_func(request, *args, **kwargs)

        return _operate_record

    return decorator
