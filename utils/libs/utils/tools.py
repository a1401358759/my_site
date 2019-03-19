# -*- coding: utf-8 -*-


def unicode2utf8(value):
    if isinstance(value, unicode):
        value = value.encode("utf-8")
    if not isinstance(value, basestring):
        value = str(value)
    return value


def utf82unicode(content):
    try:
        if not isinstance(content, basestring):
            content = str(content)
        if not isinstance(content, unicode):
            content = content.decode("utf-8")
    except:
        content = u"fail_utf8_to_unicode"
    return content


def thousands_separator(value):
    """
    千位分隔符
    例如传入 1000000000,返回 1,000,000,000
    :param value: 需要转换的数字
    :return: 格式化后的字符串
    """
    return '{:,}'.format(value)


def ten_thousands_separator(value):
    """
    千位分隔符,单位 `万`
    例如传入 1000000000,返回 100,000
    :param value: 需要转换的数字
    :return: 格式化后的字符串,单位 `万`
    """
    value /= 10000
    return thousands_separator(value)


def truncate_interger_from_decimal(value):
    """
    保留一个数字的整数部分
    返回int类型
    :param value:
    :return:
    """
    return int(float(value))


def truncate_decimal_from_decimal(value):
    """
    保留一个数字的小数部分
    返回str类型
    :param value:
    :return: str
    """
    return ("%.2f" % float(value)).split(".")[1]
