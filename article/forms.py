# -*- coding: utf-8 -*-

from django import forms


class CommentForm(forms.Form):
    nickname = forms.CharField()
    email = forms.CharField()
    website = forms.CharField(required=False)
    content = forms.CharField()
    target = forms.CharField()
    parent_comment_id = forms.IntegerField(required=False)
