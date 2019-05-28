# -*- coding: utf-8 -*-

from utils.libs.httpclient import RequestClient
from utils.libs.logger import SysLogger
from utils.libs.config.default_settings import AMAP_SERVER_KEY


def get_location_by_ip(ip):
    if not ip or ip == "127.0.0.1":
        return "", "", ""
    response = RequestClient.query(
        "http://freeapi.ipip.net/%s" % ip,
        method="GET",
        params={}
    )
    try:
        ret_json = response.json()
        country = ret_json[0]
        province = ret_json[1]
        city = ret_json[2]
        return country, province, city
    except Exception, exp:
        SysLogger.exception(exp)
        return "", "", ""


def get_location_by_ip_with_amap(ip):
    """
    使用高德API通过IP获取地理位置
    """
    response = RequestClient.query(
        "http://restapi.amap.com/v3/ip",
        method="POST",
        data={
            "ip": ip,
            "output": "JSON",
            "key": AMAP_SERVER_KEY,
        }
    )
    try:
        ret_json = response.json()
        adcode = ret_json["adcode"] or 0
        province = ret_json["province"] or ""
        city = ret_json["city"] or ""
        return adcode, province, city
    except Exception, exp:
        SysLogger.exception(exp)
        return 0, u"", u""


def get_location_by_lon_and_lat(lon, lat):
    """
    根据经纬度查询地址

    文档地址 http://lbs.amap.com/api/webservice/guide/api/georegeo/#regeo
    :param lon:
    :param lat:
    :return: ADCODE,省,市,县,屯,详细地址
    """
    if not (lon and lat):
        return 0, u"未知", u"未知", u"未知", u"未知", u"未知"
    response = RequestClient.query(
        "http://restapi.amap.com/v3/geocode/regeo",
        method="GET",
        params={
            "output": "JSON",
            "key": AMAP_SERVER_KEY,
            "location": "%s,%s" % (lon, lat),
            "radius": 1000,
            "extensions": "base",
            "batch": "false",
            "roadlevel": 1,
        }
    )
    try:
        ret_json = response.json()
        adcode = ret_json["regeocode"]['addressComponent']['adcode']
        province = ret_json["regeocode"]['addressComponent']['province']
        city = ret_json["regeocode"]['addressComponent']['city']
        district = ret_json["regeocode"]['addressComponent']['district']
        township = ret_json["regeocode"]['addressComponent']['township']
        address = ret_json["regeocode"]['formatted_address']
        return adcode, province, city, district, township, address
    except Exception, exp:
        SysLogger.exception(exp)
        return 0, u"未知", u"未知", u"未知", u"未知", u"未知"


def get_address_info(lon, lat, ip):
    """
    根据经纬度和IP查询地址

    :param lon:
    :param lat:
    :param ip:
    :return: ADCODE,省,市,县,屯,详细地址
    """
    adcode, province, city, district, township, address = "", u"未知", u"未知", "", "", ""
    if lon and lat:
        adcode, province, city, district, township, address = get_location_by_lon_and_lat(lon, lat)

    if u"未知" in (province, city):
        adcode, province, city = get_location_by_ip(ip)
    return adcode, province, city, district, township, address
