#!/usr/bin/env python
# -*- coding: utf-8  -*-
import os
from os.path import dirname as d

lib_name = os.path.basename(d(d(d(__file__))))
# logging
LOG_ROOT = '.'
PROJECT_INFO_LOG = "sep.trace_info"
PROJECT_ERROR_LOG = "sep.trace_error"
PROJECT_EXCEPTION_LOG = "sep.trace_exception"
PROJECT_HTTPCLIENT_LOG = "sep.trace_httpclient"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s:\n %(message)s'
        },
        'exception': {
            'format': '[%(asctime)s] %(levelname)s %(module)s Line:%(lineno)d:\n'
        },
        'trace_service': {
            'format': '%(message)s'
        },
    },
    'filters': {},
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        PROJECT_INFO_LOG: {
            'level': 'DEBUG',
            'class': 'utils.libs.logger.SepLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/trace_info.log"),
            'formatter': 'verbose',
            'when': 'midnight',
        },
        PROJECT_ERROR_LOG: {
            'level': 'ERROR',
            'class': 'utils.libs.logger.SepLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/trace_error.log"),
            'formatter': 'verbose',
            'when': 'midnight',
        },
        PROJECT_EXCEPTION_LOG: {
            'level': 'ERROR',
            'class': 'utils.libs.logger.SepLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/trace_exception.log"),
            'formatter': 'exception',
            'when': 'midnight',
        },
        PROJECT_HTTPCLIENT_LOG: {
            'level': 'INFO',
            'class': 'utils.libs.logger.SepLogTimedRotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "logs/trace_httpclient.log"),
            'formatter': 'trace_service',
            'when': 'midnight',
        },
    },
    'loggers': {
        PROJECT_INFO_LOG: {
            'handlers': [PROJECT_INFO_LOG],
            'level': 'DEBUG',
        },
        PROJECT_ERROR_LOG: {
            'handlers': [PROJECT_ERROR_LOG],
            'level': 'ERROR',
        },
        PROJECT_EXCEPTION_LOG: {
            'handlers': [PROJECT_EXCEPTION_LOG],
            'level': 'ERROR',
        },
        PROJECT_HTTPCLIENT_LOG: {
            'handlers': [PROJECT_HTTPCLIENT_LOG],
            'level': 'INFO',
        },
    },
}
