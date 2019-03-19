# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from utils.dlibs.forms.validators import email_validator
from article.constants import EditorKind, BlogStatus


class SearchBlogForm(forms.Form):
    title = forms.CharField(label=u'博客标题', required=False)


class LoginForm(forms.Form):
    user_name = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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


class OperateBlogForm(forms.Form):
    title = forms.CharField(label=u'标题', max_length=100)
    author = forms.IntegerField(label=u'作者')
    classification = forms.IntegerField(label=u'分类')
    content = forms.CharField(label=u'内容')
    count = forms.IntegerField(label=u'阅读量', required=False)
    editor = forms.ChoiceField(label=u'编辑器类型', choices=EditorKind.CHOICES)
    status = forms.ChoiceField(label=u'状态', choices=BlogStatus.CHOICES)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'旧密码', max_length=128, widget=forms.PasswordInput())
    new_password = forms.CharField(label=u'新密码', max_length=128, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label=u'确认新密码', required=True, max_length=128, widget=forms.PasswordInput())

    def clean_confirm_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(message='请确认两次输入的新密码一致')
        return self.cleaned_data['confirm_password']
