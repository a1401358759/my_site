# -*- coding: utf-8 -*-

from django import forms
from utils.dlibs.forms.validators import email_validator
from article.constants import EditorKind


class SearchBlogForm(forms.Form):
    title = forms.CharField(label=u'博客标题', required=False)


class AddFriendLinkForm(forms.Form):
    name = forms.CharField(label=u'网站名称')
    link = forms.CharField(label=u'网站链接')
    avatar = forms.CharField(label=u'网站图标', required=False)
    desc = forms.CharField(label=u'网站描述')


class AddAuthorForm(forms.Form):
    name = forms.CharField(label=u'作者姓名')
    email = forms.CharField(label=u'作者邮箱', required=False, validators=[email_validator])
    website = forms.CharField(label=u'个人网站', required=False)


class AddMusicForm(forms.Form):
    name = forms.CharField(label=u'音乐名称')
    url = forms.CharField(label=u'音乐地址')
    cover = forms.CharField(label=u'音乐封面')
    artist = forms.CharField(label=u'演唱者', required=False)


class AddCarouselForm(forms.Form):
    name = forms.CharField(label=u'图片名称')
    description = forms.CharField(label=u'图片描述')
    path = forms.CharField(label=u'图片路径')
    link = forms.CharField(label=u'图片外链', required=False)
    weights = forms.IntegerField(label=u'图片权重')


class OperateOwnMessageForm(forms.Form):
    summary = forms.CharField(label=u'简介')
    message = forms.CharField(label=u'寄语')
    editor = forms.ChoiceField(label=u'编辑器类型', choices=EditorKind.CHOICES)
