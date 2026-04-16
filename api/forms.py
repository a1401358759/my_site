# -*- coding: utf-8 -*-

from django import forms
from utils.dlibs.forms.base import BaseListForm


class BlogListForm(BaseListForm):
    title = forms.CharField(required=False)


class HomeFeedForm(BaseListForm):
    keyword = forms.CharField(required=False)
    tag = forms.CharField(required=False)
    classification = forms.CharField(required=False)
    year = forms.IntegerField(required=False, min_value=1970, max_value=2999)
    month = forms.IntegerField(required=False, min_value=1, max_value=12)
