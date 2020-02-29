# -*- coding: utf-8 -*-
# !/usr/bin/env python

from utils.libs.error.errorcode import CommonError, StatusCode


class ERRORCODE(CommonError):
    '''错误码
    '''
    BASE = 54000
    SEND_VERIFICATION_OVER_RATE = StatusCode(BASE + 1, 'Send verification over rate', '验证码发送频率过高')
    VERIFY_TIMES_LIMITED = StatusCode(BASE + 2, 'Verify times limited', '验证码验证次数过多')
    CAPTCHA_VERIFY_FAILURE = StatusCode(BASE + 3, "verify failure.", "验证码错误")
    REFUND_ERROR = StatusCode(BASE + 4, 'refund error', '退款失败')
