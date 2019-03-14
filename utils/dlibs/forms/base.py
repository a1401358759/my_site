# -*- coding: utf-8 -*-
from django import forms

from utils.dlibs.forms.constants import FormConstants


class BaseAdminModelForm(forms.ModelForm):
    '''admin基础model form类，admin中所有使用model form的都要直接继承此类

    扩展功能：
        1. 增加is_update属性，新建model对象时为False，更新时为True
    '''
    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.get('instance') is not None
        super(BaseAdminModelForm, self).__init__(*args, **kwargs)


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
