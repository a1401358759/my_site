#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import logging
from datetime import datetime
import requests
from requests.models import PreparedRequest

from utils.libs.error import RequestMethodError
from utils.libs.logger import SysLogger
from utils.libs.config.logger_settings import PROJECT_HTTPCLIENT_LOG

MAX_CONSUMING_TIME = 500  # 单位ms


class RequestClient(object):
    """
    封装http requests： 记录日志、重试机制、保护机制

    调用方法： RequestClient.query(url=url)
    """
    _request_session = requests.Session()     # 带有会话的请求,可以使用连接池

    @classmethod
    def _get_headers(cls, add_sep_headers, headers):
        default_headers = {}
        if add_sep_headers:  # 默认的头部
            default_headers = {
                "Accept-Language": "zh_CN",
                "User-Agent": "sep",
                "Connection": "Keep-Alive",
            }
        if headers and isinstance(headers, dict):
            default_headers.update(headers)

        return default_headers

    @classmethod
    def query(cls, url, method="POST", params=None, data={}, files={}, timeout=3, retry=1,
              headers=None, add_sep_headers=False, record_params=True, stream=False, **kwargs):
        """
            :params url: 要访问的url
            :param params: 参数In URL
            :param data: form-data数据
            :param files: POST a Multipart-Encoded File
            :param retry: 当失败时候，重试次数
            :params record_params 记录日志的时候是否需要将params/data你们的数据记录
            :return response or None
        """
        params = params if params else {}
        method = method.lower()
        times = 0
        response = None
        # get headers
        default_headers = cls._get_headers(add_sep_headers, headers)

        # method 只是支持以下几种
        if method not in ["post", "get", "put", "delete", "options", "head"]:
            raise RequestMethodError

        if method == "post" and retry > 1:
            SysLogger.warn("请确保POST请求可以重试.\n")

        while times < retry:
            start_time = time.time()
            try:
                if kwargs.get('cert'):
                    # 带证书的请求使用requests session，如果两次使用不同证书，requests只使用第一次初始化时的证书，
                    # 所以这里如果使用了证书就不使用session
                    request_mode = requests
                else:
                    request_mode = cls._request_session
                response = getattr(request_mode, method)(url=url, params=params, data=data, headers=default_headers,
                                                         files=files, timeout=timeout, stream=stream, **kwargs)
            except Exception, exp:
                SysLogger.exception(exp)

            # 400以上的错误，599以下错误，需要接着访问
            error_code = getattr(response, 'status_code', 599)
            times = times + 1 if error_code >= 400 and error_code <= 599 else times + retry
            AccessStatus(
                url=url,
                params=params,
                data=data,
                access_time=start_time,
                consuming_time=int(round((time.time() - start_time) * 1000)),  # ms
                error_code=error_code,
                method=method,
                record_params=record_params).log()
        return response


class AccessStatus(object):
    """记录access log """
    def __init__(self, url, params, data, access_time, consuming_time=0,
                 error_code=200, message="", method='', record_params=False):
        self.url = url
        self.params = params
        self.data = data
        self.access_time = access_time
        self.consuming_time = consuming_time
        self.error_code = error_code
        self.message = message
        self.method = method
        self.record_params = record_params
        self.REPORT_FUNCTION_CONF = None

    def log(self, **kwargs):
        """log记录 """
        if not self.message:
            if self.error_code >= 400:
                self.message = 'ERROR'
            elif self.error_code == 0:
                self.message = "protected"
            elif self.consuming_time >= MAX_CONSUMING_TIME:
                self.message = "Slow access"
            else:
                self.message = "Log access"

        query_time = datetime(*time.localtime(float(self.access_time))[:6])
        msg = '[{query_time}] {consuming_time}ms [{error_code} {message}] "{method} {url}{params}"'.format(
            query_time=str(query_time),
            consuming_time=self.consuming_time,
            error_code=self.error_code,
            message=self.message,
            method=self.method.upper(),
            url=self.url,
            params=self._format_args()
        )
        logger = logging.getLogger(PROJECT_HTTPCLIENT_LOG)
        if logger:
            logger.info(msg)

    def _format_args(self):
        """将params/data的数据拼接在url里 """
        if not self.record_params:
            return ''

        args_text = ""
        try:
            sign = "&" if '?' in self.url else "?"
            if self.params:
                args_text = sign + PreparedRequest._encode_params(self.params)
            elif self.data:
                args_text = sign + PreparedRequest._encode_params(self.data)
        except:
            pass

        return args_text
