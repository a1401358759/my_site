#!/usr/bin/env python
# -*- coding: utf-8  -*-

""" SysLogger日志 """

import traceback
import logging
import sys
from utils.libs.config.logger_settings import PROJECT_INFO_LOG, PROJECT_ERROR_LOG, PROJECT_EXCEPTION_LOG


class SysLogger(object):
    ''' system logger '''

    @classmethod
    def _logger_init(cls):
        cls.INFO_LOGGER = getattr(cls, 'INFO_LOGGER', logging.getLogger(PROJECT_INFO_LOG))
        cls.ERROR_LOGGER = getattr(cls, 'ERROR_LOGGER', logging.getLogger(PROJECT_ERROR_LOG))
        cls.EXCEPTION_LOGGER = getattr(cls, 'EXCEPTION_LOGGER', logging.getLogger(PROJECT_EXCEPTION_LOG))

    @classmethod
    def debug(cls, msg):
        '''
        logging debug message
        :param cls:
        :param msg:
        '''
        cls._logger_init()
        extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
        cls.INFO_LOGGER.debug(msg, extra=extra)

    @classmethod
    def info(cls, msg):
        '''
        logging info message，info类型不收集traceback
        :param cls:
        :param msg:
        '''
        cls._logger_init()
        cls.INFO_LOGGER.info(msg)

    @classmethod
    def warn(cls, msg):
        '''
        logging warn message
        :param cls:
        :param msg:
        '''
        cls._logger_init()
        extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
        cls.INFO_LOGGER.warn(msg, extra=extra)

    @classmethod
    def error(cls, msg):
        '''
        logging error message
        :param cls:
        :param msg:
        '''
        cls._logger_init()
        extra = {"realLocation": repr(traceback.format_stack(limit=2)[0])}
        cls.ERROR_LOGGER.error(msg, extra=extra)

    @classmethod
    def exception(cls, exp, request=None):
        '''
        logging exception under both error file and log file.
        :param cls:
        :param exp:
        :param request: 可以为sentry提供request信息，能传尽量传
        '''
        cls._logger_init()
        extra = {
            "realLocation": repr(traceback.format_stack(limit=2)[0]),
            "request": request
        }
        cls.INFO_LOGGER.error(exp, extra=extra)
        if sys.version_info >= (2, 7, 7):  # python2.7.7后才支持extra参数
            cls.EXCEPTION_LOGGER.exception(exp, extra=extra)
        else:
            cls.EXCEPTION_LOGGER.exception(exp)
