# -*- coding: utf-8 -*-

from django import forms
from utils.dlibs.forms.base import BaseListForm
from utils.dlibs.forms.validators import email_validator


class CommentForm(forms.Form):
    nickname = forms.CharField(label=u'昵称', max_length=20)
    email = forms.CharField(label=u'邮箱', validators=[email_validator])
    website = forms.CharField(label=u'网站', required=False, max_length=50)
    content = forms.CharField(label=u'评论内容', max_length=150)
    target = forms.CharField()
    parent_comment_id = forms.IntegerField(required=False)


class GetCommentsForm(BaseListForm):
    target = forms.CharField()
