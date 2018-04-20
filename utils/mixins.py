# -*- coding: utf-8 -*-

from django.db import models
from django.utils.functional import curry


class BaseModel(models.Model):
    '''基础Model

    目前没有实现任何逻辑，只作为配合使用其他model mixin的时候作为第一个占位，以保持field顺序
    '''
    class Meta:
        abstract = True


class TimeModelMixin(models.Model):
    '''Model内时间维护信息插件

    注意！！：因为此mixin继承自models.Model，所以子类在继承时要确保此mixin在models.Model`出现`之前使用，
    否则会出现method resolution order (MRO) 报错'''
    created_time = models.DateTimeField("创建时间", auto_now_add=True, editable=False)
    last_update = models.DateTimeField("最后修改时间", auto_now=True, editable=False)

    class Meta:
        abstract = True


class EditorModelMixin(models.Model):
    '''Model内时间维护信息插件

    注意！！：因为此mixin继承自models.Model，所以子类在继承时要确保此mixin在models.Model`出现`之前使用，
    否则会出现method resolution order (MRO) 报错'''
    creator_id = models.IntegerField("创建者")
    last_editor_id = models.IntegerField("最后修改者")

    class Meta:
        abstract = True
