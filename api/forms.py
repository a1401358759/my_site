# -*- coding: utf-8 -*-

from django import forms
from utils.dlibs.forms.base import BaseListForm


class BlogListForm(BaseListForm):
    title = forms.CharField(required=False)
