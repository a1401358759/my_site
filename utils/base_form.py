# -*- coding: utf-8 -*-
from django import forms


class FormConstants(object):
    DEFAULT_PAGE_SIZE = 10


class BaseListForm(forms.Form):
    """用于获取列表的表单,包含page_num和page_size两个参数"""
    page_num = forms.IntegerField(required=False)
    page_size = forms.IntegerField(required=False)

    def clean_page_num(self):
        """检查和处理页码"""
        page_num = self.cleaned_data['page_num'] or 1
        return page_num if page_num > 0 else 1

    def clean_page_size(self):
        """检查和处理页面大小"""
        page_size = self.cleaned_data['page_size'] or FormConstants.DEFAULT_PAGE_SIZE
        return page_size if page_size > 0 else FormConstants.DEFAULT_PAGE_SIZE
