from django import forms
from django.core.exceptions import ValidationError
from utils.dlibs.forms.validators import email_validator
from article.constants import EditorKind, BlogStatus, CarouselImgType


class SearchBlogForm(forms.Form):
    title = forms.CharField(label='博客标题', required=False)


class LoginForm(forms.Form):
    user_name = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddFriendLinkForm(forms.Form):
    edit_id = forms.IntegerField(label='link_id', required=False)
    name = forms.CharField(label='网站名称')
    link = forms.CharField(label='网站链接')
    avatar = forms.CharField(label='网站图标', required=False)
    desc = forms.CharField(label='网站描述')


class AddAuthorForm(forms.Form):
    item_id = forms.IntegerField(required=False)
    name = forms.CharField(label='作者姓名')
    email = forms.CharField(label='作者邮箱', required=False, validators=[email_validator])
    website = forms.CharField(label='个人网站', required=False)


class AddMusicForm(forms.Form):
    name = forms.CharField(label='音乐名称')
    url = forms.CharField(label='音乐地址')
    cover = forms.CharField(label='音乐封面')
    artist = forms.CharField(label='演唱者', required=False)


class AddCarouselForm(forms.Form):
    name = forms.CharField(label='图片名称')
    description = forms.CharField(label='图片描述')
    path = forms.FileField(label='图片')
    link = forms.CharField(label='图片外链', required=False)
    img_type = forms.ChoiceField(label='图片类型', choices=CarouselImgType.CHOICES)
    weights = forms.IntegerField(label='图片权重')


class OperateOwnMessageForm(forms.Form):
    summary = forms.CharField(label='简介')
    message = forms.CharField(label='寄语')
    editor = forms.ChoiceField(label='编辑器类型', choices=EditorKind.CHOICES)


class OperateBlogForm(forms.Form):
    title = forms.CharField(label='标题', max_length=100)
    author = forms.IntegerField(label='作者')
    classification = forms.IntegerField(label='分类')
    content = forms.CharField(label='内容')
    count = forms.IntegerField(label='阅读量', required=False)
    editor = forms.ChoiceField(label='编辑器类型', choices=EditorKind.CHOICES)
    status = forms.ChoiceField(label='状态', choices=BlogStatus.CHOICES)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧密码', max_length=128, widget=forms.PasswordInput())
    new_password = forms.CharField(label='新密码', max_length=128, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='确认新密码', required=True, max_length=128, widget=forms.PasswordInput())

    def clean_confirm_password(self):
        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(message='请确认两次输入的新密码一致')
        return self.cleaned_data['confirm_password']


class UpdateBlogStatusForm(forms.Form):
    blog_id = forms.IntegerField(label='博客id')
    status = forms.ChoiceField(label='状态', choices=BlogStatus.CHOICES)
