# -*- coding: utf-8 -*-

import re


class Validate(object):
    """docstring for Validate"""
    def __init__(self, arg):
        super(Validate, self).__init__()
        self.arg = arg

    # 正则匹配电话号码
    def validate_phone(phone_num):
        if not phone_num:
            return False
        pattern = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        if pattern.match(phone_num):
            return True
        else:
            return False

    # 正则表达式验证邮箱
    def validate_email(email):
        if not email:
            return False
        pattern = re.compile('^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$')
        if pattern.match(email):
            return True
        else:
            return False
