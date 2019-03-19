# -*- coding: utf-8 -*-

import requests
from utils.libs.logger.syslogger import SysLogger
from utils.libs.config.default_settings import AMAP_SERVER_KEY


def form_error(form_info):
    error_str = []
    for k, v in form_info.errors.items():
        if k == "__all__":
            error_str.append(v[0])
        else:
            error_str.append(u"%s:%s" % (form_info.fields[k].label, v[0]))

    return error_str


def get_lon_lat_by_address(address):
    """
    使用高德API通过地址获取经纬度(lon, lat)
    """
    par = {'address': address, 'key': AMAP_SERVER_KEY}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    try:
        GPS = answer['geocodes'][0]['location'].split(",")
        return GPS[0], GPS[1]
    except Exception as exp:
        SysLogger.exception(exp)
        return None, None
