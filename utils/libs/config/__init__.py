# -*- coding: utf-8  -*-
"""
注意:这里的配置需要在具体项目的config.libs_settings中进行重新定义,
如果没有重新定义,那么此处定义的配置就会生效.
"""
from utils.libs.settings import LazySettings
from . import default_settings

# 配置项目中的libs相关配置的规定存储位置
libs_settings_path = "config.libs_settings"

settings = LazySettings(libs_settings_path, default_settings)
