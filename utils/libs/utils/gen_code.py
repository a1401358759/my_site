# -*- coding: utf-8 -*-
'''生成各种编码'''

import time
import datetime
from Crypto.Random import random


class CODE_TYPE(object):
    '''编号类型'''
    FLOW = 1
    ORDER = 2


def generate_ts_unique_code(code_type):
    '''基于时间戳（精确到秒）和随机数(5位)生成唯一编号，16位

    编号规则：编号类型（1位）+  时间戳（10位，到秒）+ 随机数（5位）

    :param code_type -- 编号类型
    '''
    rand_num = random.randint(0, 99999)
    return "%01d%d%05d" % (code_type, int(time.time()), rand_num)


def generate_datetime_unique_code(code_type):
    '''基于时间格式（精确到秒）和随机数（5位）生成唯一编号，18位

    适合生成码量不会很频繁，又想快速看时间的场景
    编号规则：编号类型（1位）+ 时间（12位，年后两位+月日时分秒，如161018235959）+ 随机数（5位）

    :param code_type -- 编号类型
    '''
    rand_num = random.randint(0, 99999)
    datetime_str = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    return "%01d%s%05d" % (code_type, datetime_str, rand_num)


def _generate_unique_code(code_type, service_type):
    '''基于时间戳（精确到秒）和随机数(5位)生成唯一编号，18位

    编号规则：编号类型（1位）+ 服务类型（2位）+ 时间戳（10位，到秒）+ 随机数（5位），共18位

    :param code_type -- 编号类型，详见CODE_TYPE
    :param service_type -- 业务类型
    '''
    rand_num = random.randint(0, 99999)
    return "%s%02d%d%05d" % (code_type, service_type, int(time.time()), rand_num)


def generate_flow_code(service_type):
    """
    生成流水号，流水号长度18位

    编号规则：1 + 业务类型（2位）+ 时间戳（10位，到秒）+ 随机数（5位），共18位

    :param service_type -- 业务类型
    """
    return _generate_unique_code(CODE_TYPE.FLOW, service_type)


def generate_order_code(service_type):
    """
    生成订单号，订单号长度18位

    编号规则：2 + 业务类型（2位）+ 时间戳（10位，到秒）+ 随机数（5位），共18位

    :param service_type -- 业务类型
    """
    return _generate_unique_code(CODE_TYPE.ORDER, service_type)


def generate_datetime_order_code(service_type):
    """
    日期格式订单号，长度18位
    编号规则：订单业务类型（1位，订单业务类型）+ 时间（12位，年后两位+月日时分秒，如161018235959）+ 随机数（5位）

    :param service_type -- 业务类型
    """
    return generate_datetime_unique_code(service_type)
