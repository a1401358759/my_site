# -*- coding: utf-8 -*-

from django import forms


class SearchBlogForm(forms.Form):
    title = forms.CharField(label=u'博客标题', required=False)
