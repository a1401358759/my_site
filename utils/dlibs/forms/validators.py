# -*- coding: utf-8 -*-
import re

from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


# --------------- 正则表达式 ------------------#
# 手机号：T开头的手机号（T替换1）用于自动化测试，校验通过，但不发短信
_white_num = '[T1][3456789]\d{9}'
mobile_rex = r"^(?:\+?86[- ]?|0)?(%s)$" % _white_num
MOBILE_RE = re.compile(mobile_rex)
# 手机验证码: 6位纯数字
VERIFY_CODE_RE = re.compile(r"^\d{6}$")
# 图形验证码: 4位纯字母
CAPTCHA_RE = re.compile(r"^\d{4}$")
# 身份证
ID_NUM_RE = re.compile(r'^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X|x)$')


# --------------- validators ------------------#
mobile_validator = RegexValidator(MOBILE_RE, u'手机号格式不正确', 'invalid')
email_validator = EmailValidator(u'请输入正确的email', 'invalid')
verify_code_validator = RegexValidator(VERIFY_CODE_RE, u'短信验证码格式不正确', 'invalid')
captcha_validator = RegexValidator(CAPTCHA_RE, u'图片验证码格式不正确', 'invalid')
id_num_validator = RegexValidator(ID_NUM_RE, u'身份证号码错误', 'invalid')


# --------------- 验证函数 ------------------#
def is_valid_mobile(mobile):
    '''验证手机号
    '''
    if not mobile:
        return False
    try:
        mobile_validator(mobile)
        return True
    except ValidationError:
        return False
