# -*- coding: utf-8 -*-

from django import forms


class CommentForm(forms.Form):
    nickname = forms.CharField(label=u'昵称')
    email = forms.CharField(label=u'邮箱')
    website = forms.CharField(label=u'网站', required=False)
    content = forms.CharField(label=u'评论内容')
    target = forms.CharField()
    parent_comment_id = forms.IntegerField(required=False)
