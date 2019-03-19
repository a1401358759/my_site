# -*- coding: utf-8 -*-
'''只定义最基础的exception，业务级exception直接初始化APIError，*不要*再定义新业务级exception'''

from .errorcode import CommonError


class ImproperlyConfigured(Exception):
    """Django is somehow improperly configured"""
    pass


class APIError(Exception):
    '''业务级exception直接初始化此类，*不要*再定义新业务级exception类'''
    statuscode = CommonError.UNKNOWN

    def __init__(self, statuscode=None, msg=None, msgcn=None):
        if statuscode is not None:
            self.statuscode = statuscode
        if msg is not None:
            self.statuscode.msg = msg
        if msgcn is not None:
            self.statuscode.msgcn = msgcn

    def __repr__(self):
        return '%s(code=%r, message=%r, msgcn=%r)' % (self.__class__,
                                                      self.statuscode.code,
                                                      self.statuscode.msg,
                                                      self.statuscode.msgcn)

    def as_dict(self):
        return {'code': self.statuscode.code, 'msg': self.statuscode.msg, 'msgcn': self.statuscode.msgcn}


class RequestMethodError(Exception):
    def __repr__(self):
        return "request method not allowed."
