# -*- coding: utf-8  -*-
'''
实现错误码基础类`StatusCode`的格式和公共错误码类`CommonStatus`
'''


class StatusCode(object):
    '''错误码基础类

    每个错误码有code, msg和msgcn三个属性,
    三个属性同时支持StatusCode.code式属性方式获取，也支持StatusCode['code']式的字典key方式获取.
    '''
    def __init__(self, code, msg, msgcn=''):
        '''
        code -- 错误码, int
        msg -- 英文错误信息, str
        msgcn -- 中文错误信息, str
        '''
        self._code = int(code)
        self._msg = msg
        self._msgcn = msgcn

    def __str__(self):
        return self._msg

    def __int__(self):
        return self._code

    def __ne__(self, other):
        if hasattr(other, 'code'):
            return self._code != other.code
        else:
            try:
                return self._code != int(other)
            except:
                return self._code != other

    def __eq__(self, other):
        if hasattr(other, 'code'):
            return self._code == other.code
        else:
            try:
                return self._code == int(other)
            except:
                return self._code == other

    def __getitem__(self, key):
        if key == 'code':
            return self._code
        elif key == 'msg':
            return self._msg
        elif key == 'msgcn':
            return self._msgcn
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 'code':
            self._code = value
        elif key == 'msg':
            self._msg = value
        elif key == 'msgcn':
            self._msgcn = value
        else:
            raise KeyError

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    @property
    def msgcn(self):
        return self._msgcn

    @msgcn.setter
    def msgcn(self, value):
        self._msgcn = value


class CommonError(object):
    '''
    错误码，各系统需要继承此类，增加各自的业务错误码

    规则：子系统编码(2位. 00表示各子系统通用错误码) + 错误编码(3位)，共5位

    示例：
    class ERROR(CommonError):
        ACCOUNT_BASE = 10000
        CUSTOM_ERROR = StatusCode(ACCOUNT_BASE + 1, 'Some error msg.', u'一些错误信息.')
    '''
    COMMON_BASE = 00000
    SUCCESS = StatusCode(COMMON_BASE + 0, 'Successful.', u'成功.')
    UNKNOWN = StatusCode(COMMON_BASE + 1, 'Unknown error.', u'未知错误.')
    FAILED = StatusCode(COMMON_BASE + 2, 'Failed.', u'失败.')
    UPGRADING = StatusCode(COMMON_BASE + 3, 'System is upgrading.', u'系统升级中.')
    SERVER_TOO_BUSY = StatusCode(COMMON_BASE + 4, 'Server is too busy.', u'服务器繁忙')  # 限流
    NOT_IMPLEMENTED = StatusCode(COMMON_BASE + 5, 'Not Implemented.', u'功能尚未开放')
    IN_BLACKLIST = StatusCode(COMMON_BASE + 6, 'Illegal, Denial of service.', u'黑名单中，禁止访问')  # 黑名单
    SIGN_ERROR = StatusCode(COMMON_BASE + 7, 'Sign verification failed.', u'签名不正确')
    TIMESTAMP_EXPIRED = StatusCode(COMMON_BASE + 8, 'Timestamp expired.', u'时间戳过期')
    REQUEST_TOO_OFTEN = StatusCode(COMMON_BASE + 9, 'Request too often.', u'请求太频繁')
    PERMISSION_DENIED = StatusCode(COMMON_BASE + 10, 'Sorry, Permission Denied.', u'权限不足')
    PARAM_NOT_ENOUGH = StatusCode(COMMON_BASE + 11, 'Params not enough.', u'参数不足')
    PARAM_ERROR = StatusCode(COMMON_BASE + 12, 'Params error.', u'参数错误')
    NOT_FOUND = StatusCode(COMMON_BASE + 13, 'Not found.', u'未找到')
    NOT_LOGIN = StatusCode(COMMON_BASE + 14, 'Not login.', u'未登录')
    USER_DEACTIVE = StatusCode(COMMON_BASE + 15, 'User is deactive.', u'用户被禁用')
    WEIXIN_NOT_LOGIN = StatusCode(COMMON_BASE + 16, 'Weixin Not login.', u'微信未登录')
    SUPERUSER_PERMISSION_DENIED = StatusCode(COMMON_BASE + 17, 'Sorry,Superuser Permission Denied.', u'超级管理员权限不足')
    WALLET_NOT_ENOUGH = StatusCode(COMMON_BASE + 18, 'wallet not enough', u'钱包余额不足')
