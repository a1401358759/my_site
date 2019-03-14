# -*- coding: utf-8 -*-

from django.db import models


class BaseModel(models.Model):
    """基础Model

    目前没有实现任何逻辑，只作为配合使用其他model mixin的时候作为第一个占位，以保持field顺序
    """
    class Meta:
        abstract = True
