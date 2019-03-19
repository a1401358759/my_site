# -*- coding: utf-8 -*-

import urllib
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from utils.errorcode import ERRORCODE
from utils.dlibs.http.response import http_response
from utils.dlibs.tools.paginator import paginate
from utils.common import form_error
from article.models import (
    Article, Links, Classification, CarouselImg,
    Music, Author, OwnerMessage, Tag
)
from article.constants import EditorKind, BlogStatus
from .forms import (
    SearchBlogForm, AddFriendLinkForm, OperateOwnMessageForm, LoginForm,
    AddAuthorForm, AddMusicForm, AddCarouselForm, OperateBlogForm, ChangePasswordForm
)


def login_view(request):
    """
    用户登录
    :param request:
    :return:
    """
    back_url = request.parameters.get('back_url')
    if not back_url:
        back_url = reverse('blog_list')
    user_info = request.session.get('user_info')
    if user_info:
        return HttpResponseRedirect(back_url)

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'manager/login.html', {"back_url": back_url, "form": form})

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.warning(request, u'登录失败')
            return HttpResponseRedirect(reverse('login_view'))

        user_name = form.cleaned_data.get('user_name')
        password = form.cleaned_data.get('password')
        user = authenticate(username=user_name, password=password)
        if not user:
            messages.error(request, u'登录失败，请检查用户名密码后重试.')
            return HttpResponseRedirect('%s?%s' % (reverse('login_view'), urllib.urlencode({'back_url': back_url})))
        login(request, user)
        return HttpResponseRedirect(reverse('blog_list'))


@login_required
def logout_view(request):
    """
    用户登出
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect('/manager')


@login_required
def change_passwd_view(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            if user.check_password(form.cleaned_data['old_password']):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                messages.success(request, u'密码修改成功，请重新登录')
                return HttpResponseRedirect(reverse("logout_view"))
            else:
                messages.error(request, u'原密码错误.')
                return HttpResponseRedirect(reverse('change_password'))
    else:
        form = ChangePasswordForm()
    data = {
        'form': form
    }
    return render(request, "manager/change_password.html", data)


@login_required
def blog_list_view(request):
    """
    博客列表
    :param request:
    :return:
    """
    form = SearchBlogForm(request.GET)
    form.is_valid()
    query = Q()
    title = form.cleaned_data.get("title")
    if title:
        query &= (Q(title__icontains=title) | Q(classification__name=title) | Q(tags__name=title))

    blogs = Article.objects.select_related().filter(query).order_by("-id")
    blog_list, total = paginate(
        blogs,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/blog_list.html', {
        "active_classes": ['.blog', '.blog_list'],
        "params": request.GET,
        "form": form,
        "data_list": blog_list,
        "total": total,
    })


@login_required
def blog_create_view(request):
    """
    博客添加
    """
    tp = "manager/create_blog.html"
    auhtors = Author.objects.values("id", "name")
    classifications = Classification.objects.values("id", "name")
    tags = Tag.objects.values("id", "name")
    context = {
        "active_classes": ['.blog', '.blog_list'],
        "auhtors": auhtors,
        "classifications": classifications,
        "tags": tags,
        "blog_status": BlogStatus.CHOICES,
    }
    if request.method == "GET":
        return render(request, tp, context)

    if request.method == "POST":
        form = OperateBlogForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "</br>".join(form_error(form)))
            return HttpResponseRedirect(reverse('blog_list'))
        try:
            article = Article.objects.create(
                title=form.cleaned_data.get("title"),
                author_id=form.cleaned_data.get("author"),
                classification_id=form.cleaned_data.get("classification"),
                content=form.cleaned_data.get("content"),
                count=form.cleaned_data.get("count"),
                status=form.cleaned_data.get("status"),
                editor=EditorKind.Markdown,
            )
            tags = request.POST.getlist('tags')
            article.set_tags(tags)
            messages.success(request, u'添加成功')
            return HttpResponseRedirect(reverse('blog_list'))
        except Exception as ex:
            messages.warning(request, ex)
            return HttpResponseRedirect(reverse('blog_list'))


@login_required
def blog_edit_view(request, item_id):
    """
    博客编辑
    :param request:
    :return:
    """
    article = Article.objects.filter(id=item_id).first()
    if not article:
        messages.warning(request, "此博客不存在")
        return HttpResponseRedirect(reverse('blog_list'))

    selected_tags = article.get_tags()
    auhtors = Author.objects.values("id", "name")
    classifications = Classification.objects.values("id", "name")
    tags = Tag.objects.values("id", "name")
    context = {
        "active_classes": ['.blog', '.blog_list'],
        "article": article,
        "auhtors": auhtors,
        "classifications": classifications,
        "tags": tags,
        "selected_tags": selected_tags,
        "blog_status": BlogStatus.CHOICES,
        "item_id": item_id
    }
    if request.method == "GET":
        return render(request, "manager/edit_blog.html", context)

    if request.method == "POST":
        form = OperateBlogForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "</br>".join(form_error(form)))
            return HttpResponseRedirect(reverse('blog_list'))

        try:
            new_tags = request.POST.getlist('tags')
            article.set_tags(new_tags)
            Article.objects.filter(id=item_id).update(
                title=form.cleaned_data.get("title"),
                author_id=form.cleaned_data.get("author"),
                classification_id=form.cleaned_data.get("classification"),
                content=form.cleaned_data.get("content"),
                count=form.cleaned_data.get("count"),
                status=form.cleaned_data.get("status"),
                editor=form.cleaned_data.get("editor"),
            )
            messages.success(request, u'修改成功')
            return HttpResponseRedirect(reverse('blog_list'))
        except Exception, ex:
            messages.warning(request, ex)
            return HttpResponseRedirect(reverse('blog_list'))


@login_required
def blog_del_view(request):
    """
    删除博客
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        Article.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)


@login_required
def friend_link_list_view(request):
    """
    友情链接列表
    :param request:
    :return:
    """
    query = Q()
    name = request.GET.get('name')
    if name:
        query &= Q(name__icontains=name)

    links = Links.objects.filter(query).order_by("-id")
    link_list, total = paginate(
        links,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/link_list.html', {
        "active_classes": ['.blog', '.link_list'],
        "params": request.GET,
        "data_list": link_list,
        "total": total,
        "name": name
    })


@login_required
def add_friend_link_view(request):
    """
    添加友情链接
    """
    form = AddFriendLinkForm(request.POST)
    if not form.is_valid():
        messages.warning(request, "</br>".join(form_error(form)))
        return HttpResponseRedirect(reverse('friend_link_list'))

    try:
        Links.objects.create(
            name=form.cleaned_data.get('name'),
            link=form.cleaned_data.get('link'),
            avatar=form.cleaned_data.get('avatar'),
            desc=form.cleaned_data.get('desc'),
        )
        messages.success(request, u'添加成功')
        return HttpResponseRedirect(reverse('friend_link_list'))
    except Exception as e:
        messages.error(request, u'添加失败: %s' % e)
        return HttpResponseRedirect(reverse('friend_link_list'))


@login_required
def del_friend_link_view(request):
    """
    删除友情链接
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        Links.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)


@login_required
def author_list_view(request):
    """
    作者列表
    :param request:
    :return:
    """
    query = Q()
    name = request.GET.get('name')
    if name:
        query &= Q(name__icontains=name)

    authors = Author.objects.filter(query).order_by("-id")
    author_list, total = paginate(
        authors,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/author_list.html', {
        "active_classes": ['.blog', '.author_list'],
        "params": request.GET,
        "data_list": author_list,
        "total": total,
        "name": name
    })


@login_required
def add_author_view(request):
    """
    添加作者
    """
    form = AddAuthorForm(request.POST)
    if not form.is_valid():
        messages.warning(request, "</br>".join(form_error(form)))
        return HttpResponseRedirect(reverse('author_list'))

    try:
        Author.objects.create(
            name=form.cleaned_data.get('name'),
            email=form.cleaned_data.get('email'),
            website=form.cleaned_data.get('website'),
        )
        messages.success(request, u'添加成功')
        return HttpResponseRedirect(reverse('author_list'))
    except Exception as e:
        messages.error(request, u'添加失败: %s' % e)
        return HttpResponseRedirect(reverse('author_list'))


@login_required
def del_author_view(request):
    """
    删除作者
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        Author.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)


@login_required
def classification_list_view(request):
    """
    文章分类列表
    :param request:
    :return:
    """
    query = Q()
    name = request.GET.get('name')
    if name:
        query &= Q(name__icontains=name)

    classifications = Classification.objects.filter(query).order_by("-id")
    classification_list, total = paginate(
        classifications,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/classification_list.html', {
        "active_classes": ['.blog', '.classification_list'],
        "params": request.GET,
        "data_list": classification_list,
        "total": total,
        "name": name
    })


@login_required
def add_classification_view(request):
    """
    添加文章分类
    """
    try:
        Classification.objects.create(
            name=request.POST.get('name')
        )
        messages.success(request, u'添加成功')
        return HttpResponseRedirect(reverse('classification_list'))
    except Exception as e:
        messages.error(request, u'添加失败: %s' % e)
        return HttpResponseRedirect(reverse('classification_list'))


@login_required
def del_classification_view(request):
    """
    删除文章分类
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        Classification.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)


@login_required
def tag_list_view(request):
    """
    文章标签列表
    :param request:
    :return:
    """
    query = Q()
    name = request.GET.get('name')
    if name:
        query &= Q(name__icontains=name)

    tags = Tag.objects.filter(query).order_by("-id")
    tag_list, total = paginate(
        tags,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/tag_list.html', {
        "active_classes": ['.blog', '.tag_list'],
        "params": request.GET,
        "data_list": tag_list,
        "total": total,
        "name": name
    })


@login_required
def add_tag_view(request):
    """
    添加文章标签
    """
    try:
        Tag.objects.create(
            name=request.POST.get('name')
        )
        messages.success(request, u'添加成功')
        return HttpResponseRedirect(reverse('tag_list'))
    except Exception as e:
        messages.error(request, u'添加失败: %s' % e)
        return HttpResponseRedirect(reverse('tag_list'))


@login_required
def del_tag_view(request):
    """
    删除文章标签
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        Tag.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)


@login_required
def music_list_view(request):
    """
    背景音乐列表
    :param request:
    :return:
    """
    query = Q()
    name = request.GET.get('name')
    if name:
        query &= Q(name__icontains=name)

    musics = Music.objects.filter(query).order_by("-id")
    music_list, total = paginate(
        musics,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/music_list.html', {
        "active_classes": ['.blog', '.music_list'],
        "params": request.GET,
        "data_list": music_list,
        "total": total,
        "name": name
    })


@login_required
def add_music_view(request):
    """
    添加背景音乐
    """
    form = AddMusicForm(request.POST)
    if not form.is_valid():
        messages.error(request, "</br>".join(form_error(form)))
        return HttpResponseRedirect(reverse('music_list'))
    try:
        Music.objects.create(
            name=form.cleaned_data.get('name'),
            url=form.cleaned_data.get('url'),
            cover=form.cleaned_data.get('cover'),
            artist=form.cleaned_data.get('artist'),
        )
        messages.success(request, u'添加成功')
        return HttpResponseRedirect(reverse('music_list'))
    except Exception as e:
        messages.error(request, u'添加失败: %s' % e)
        return HttpResponseRedirect(reverse('music_list'))


@login_required
def del_music_view(request):
    """
    删除背景音乐
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        Music.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)


@login_required
def carousel_list_view(request):
    """
    轮播图片列表
    :param request:
    :return:
    """
    query = Q()
    name = request.GET.get('name')
    if name:
        query &= Q(name__icontains=name)

    carousels = CarouselImg.objects.filter(query).order_by("-id")
    carousel_list, total = paginate(
        carousels,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/carousel_list.html', {
        "active_classes": ['.blog', '.carousel_list'],
        "params": request.GET,
        "data_list": carousel_list,
        "total": total,
        "name": name
    })


@login_required
def add_carousel_view(request):
    """
    添加轮播图片
    """
    form = AddCarouselForm(request.POST)
    if not form.is_valid():
        messages.error(request, "</br>".join(form_error(form)))
        return HttpResponseRedirect(reverse('carousel_list'))
    try:
        CarouselImg.objects.create(
            name=form.cleaned_data.get('name'),
            description=form.cleaned_data.get('description'),
            path=form.cleaned_data.get('path'),
            link=form.cleaned_data.get('link'),
            weights=form.cleaned_data.get('weights'),
        )
        messages.success(request, u'添加成功')
        return HttpResponseRedirect(reverse('carousel_list'))
    except Exception as e:
        messages.error(request, u'添加失败: %s' % e)
        return HttpResponseRedirect(reverse('carousel_list'))


@login_required
def del_carousel_view(request):
    """
    删除轮播图片
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        CarouselImg.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)


@login_required
def ownmessage_list_view(request):
    messages = OwnerMessage.objects.order_by("-id")
    ownmessage_list, total = paginate(
        messages,
        request.GET.get('page') or 1
    )

    return render(request, 'manager/ownmessage_list.html', {
        "active_classes": ['.blog', '.ownmessage_list'],
        "params": request.GET,
        "data_list": ownmessage_list,
        "total": total,
    })


@login_required
def add_ownmessage_view(request):
    tp = "manager/create_ownmessage.html"
    context = {
        "active_classes": ['.blog', '.ownmessage_list'],
    }
    if request.method == "GET":
        return render(request, tp, context)

    if request.method == "POST":
        form = OperateOwnMessageForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "</br>".join(form_error(form)))
            return HttpResponseRedirect(reverse('ownmessage_list'))
        try:
            OwnerMessage.objects.create(
                summary=form.cleaned_data.get("summary"),
                message=form.cleaned_data.get("message"),
                editor=EditorKind.Markdown
            )
            messages.success(request, u'添加成功')
            return HttpResponseRedirect(reverse('ownmessage_list'))
        except Exception as ex:
            messages.warning(request, ex)
            return HttpResponseRedirect(reverse('ownmessage_list'))


@login_required
def edit_ownmessage_view(request, item_id):
    """
    主人寄语编辑
    :param request:
    :return:
    """
    message = OwnerMessage.objects.filter(id=item_id).first()
    if not message:
        messages.warning(request, "此主人寄语不存在")
        return HttpResponseRedirect(reverse('ownmessage_list'))
    tp = "manager/edit_ownmessage.html"
    context = {
        "active_classes": ['.blog', '.ownmessage_list'],
        "message": message,
        "item_id": item_id
    }
    if request.method == "GET":
        return render(request, tp, context)

    if request.method == "POST":
        form = OperateOwnMessageForm(request.POST)
        if not form.is_valid():
            messages.warning(request, "</br>".join(form_error(form)))
            return HttpResponseRedirect(reverse('ownmessage_list'))
        data = {
            "summary": form.cleaned_data.get("summary"),
            "message": form.cleaned_data.get("message"),
            "editor": form.cleaned_data.get("editor")
        }
        try:
            OwnerMessage.objects.filter(id=item_id).update(**data)
            messages.success(request, u'修改成功')
            return HttpResponseRedirect(reverse('ownmessage_list'))
        except Exception, ex:
            messages.warning(request, ex)
            return HttpResponseRedirect(reverse('ownmessage_list'))


@login_required
def del_ownmessage_view(request):
    """
    删除主人寄语
    """
    item_ids = request.POST.getlist('item_ids')
    if not item_ids:
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg=u'参数错误')

    try:
        OwnerMessage.objects.filter(id__in=item_ids).delete()
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as e:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=u'删除失败: %s' % e)
