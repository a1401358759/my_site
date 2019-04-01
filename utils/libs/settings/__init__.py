# -*- coding: utf-8 -*-
"""
这是借鉴Django简化的settings配置模块.
这个配置模块,用于像libs,sdks这样的库.它使这些库本身可以拥有一个默认配置,同时使用库的项目可以指定一个指定配置.
拥有默认配置的好处之一,是测试用例方便编写.
"""

import importlib

from utils.libs.utils.lazy import LazyObject, empty


class ImproperlyConfigured(Exception):
    """Django is somehow improperly configured"""
    pass


class LazySettings(LazyObject):
    """
    一个默认设置和指定设置模块的惰性代理类.
    """
    def __init__(self, settings_module_path, default_settings_module):
        """
        初始化方法
        """
        super(LazySettings, self).__init__()
        self.settings_module_path = settings_module_path
        self.default_settings_module = default_settings_module

    def _setup(self, name=None):
        """
        加载配置信息,本方法只在配置信息第一次被使用时被调用.
        """
        if not self.settings_module_path:
            desc = ("setting %s" % name) if name else "settings"
            raise ImproperlyConfigured(
                "Requested %s, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call settings.configure() before accessing settings."
                % (desc, self.settings_module_path))
        self._wrapped = Settings(self.settings_module_path, self.default_settings_module)

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Settings'.
        if self._wrapped is empty:
            return '<LazySettings [Unevaluated]>'
        return '<LazySettings "%(settings_module)s">' % {
            'settings_module': self._wrapped.SETTINGS_MODULE,
        }

    def __getattr__(self, name):
        if name == 'settings_module_path':
            return self._settings_module_path
        if name == 'default_settings_module':
            return self._default_settings_module
        if self._wrapped is empty:
            self._setup(name)
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if name == 'settings_module_path':
            self.__dict__['_settings_module_path'] = value
        elif name == 'default_settings_module':
            self.__dict__['default_settings_module'] = value
        else:
            super(LazySettings, self).__setattr__(name, value)

    @property
    def configured(self):
        """
        Returns True if the settings have already been configured.
        """
        return self._wrapped is not empty


class Settings(object):
    def __init__(self, settings_module_path, default_settings_module):
        # 加载默认配置模块,并更新指定的配置模块中的配置项,注意:只有全部为大写的配置项会被更新.
        for setting in dir(default_settings_module):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings_module, setting))

        # 从项目的配置模块中加载相关配置信息
        self.SETTINGS_MODULE = settings_module_path
        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)

            self._explicit_settings = set()
            for setting in dir(mod):
                if setting.isupper():
                    setting_value = getattr(mod, setting)
                    setattr(self, setting, setting_value)
                    self._explicit_settings.add(setting)
        except ImportError:
            # 在开发库的时候,不会因为缺少项目中真实的配置文件而报错
            print "\033[1;33;40m### 缺少配置文件:%s | (如果是跑测试用例,可以忽略这个错误) \n\033[0m" % self.SETTINGS_MODULE

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }
