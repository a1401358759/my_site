# -*- coding: utf-8 -*-

import json
from django.db.models import F
from django.contrib.syndication.views import Feed  # 订阅RSS
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from utils.paginate import paginate
from utils.response import render_json
from .models import Article, Classification, Messages, OwnerMessage, Tag, Links
from .constants import BlogStatus
from utils.cos import Cos, TencentCosConf


def upload_file(filestream, file_name=None, dir_name=None):
    """
    tinymce上传图片
    Arguments:
        filestream {[type]} -- [文件对象]
        real_file_path {[type]} -- [文件本地路径]
        file_name {[type]} -- [文件名]
    Keyword Arguments:
        dir_name {[type]} -- [上传的文件夹] (default: {None})
    Returns:
    """
    print 111111111111
    cos_client = Cos(**TencentCosConf)
    bucket = cos_client.get_bucket("pic-1256044091")
    if file_name:
        file_name = file_name
    else:
        file_name = filestream.name.split('.')[0]
    response = bucket.upload_file(filestream, file_name, dir_name)
    return render_json({"error": False, "path": response.get("access_url")})


def home(request):
    is_home = True
    articles = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by("-publish_time")
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    new_post = Article.objects.order_by('-count')[:10]

    # 友情链接
    links = Links.objects.all().order_by("-weights", "id")
    classification = Classification.class_list.get_classify_list()  # 分类,以及对应的数目
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()  # 按月归档,以及对应的文章数目

    return render(request, 'blog/index.html', locals())


def detail(request, year, month, day, id):
    try:
        article = Article.objects.get(id=str(id))
        Article.objects.filter(id=id).update(count=F('count') + 1)
    except Article.DoesNotExist:
        raise Http404

    new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
    links = Links.objects.all().order_by("-weights", "id")
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()

    return render(request, 'blog/content.html', locals())


def archive_month(request, year, month):
    is_arch_month = True

    articles = Article.objects.filter(publish_time__year=year, publish_time__month=month, status=BlogStatus.PUBLISHED)  # 当前日期下的文章列表
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    links = Links.objects.all().order_by("-weights", "id")
    new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()

    return render(request, 'blog/index.html', locals())


def classfiDetail(request, classfi):
    is_classfi = True
    temp = Classification.objects.get(name=classfi)  # 获取全部的Article对象

    articles = temp.article_set.filter(status=BlogStatus.PUBLISHED)
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    links = Links.objects.all().order_by("-weights", "id")
    new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()

    return render(request, 'blog/index.html', locals())


def tagDetail(request, tag):
    is_tag = True
    temp = Tag.objects.get(name=tag)  # 获取全部的Article对象
    # articles = Article.objects.filter(tags=tag)
    articles = temp.article_set.filter(status=BlogStatus.PUBLISHED)
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    links = Links.objects.all().order_by("-weights", "id")
    new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()

    return render(request, 'blog/index.html', locals())


def about(request):
    articles = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-publish_time')
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    links = Links.objects.all().order_by("-weights", "id")
    new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()

    return render(request, 'blog/about.html', locals())


def archive(request):
    articles = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-publish_time')
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    links = Links.objects.all().order_by("-weights", "id")
    archive = Article.date_list.get_article_by_archive()
    new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()

    return render(request, 'blog/archive.html', locals())


class RSSFeed(Feed):
    title = "RSS feed - Daniel的小站"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    @classmethod
    def items(cls):
        return Article.objects.order_by('-publish_time')

    def item_title(self, item):
        return item.title

    @classmethod
    def item_pubdate(cls, item):
        return item.publish_time

    @classmethod
    def item_description(cls, item):
        return item.content


def blog_search(request):  # 实现对文章标题的搜索

    is_search = True
    new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:10]
    links = Links.objects.all().order_by("-weights", "id")
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()
    error = False
    if 's' in request.POST:
        s = request.POST['s']
        if not s:
            return render(request, 'blog/index.html')
        else:
            articles = Article.objects.filter(title__icontains=s)
            page_num = request.GET.get("page") or 1
            page_size = request.GET.get("page_size") or 5
            articles, total = paginate(articles, page_num=page_num, page_size=page_size)
            if len(articles) == 0:
                error = True

    return render(request, 'blog/index.html', locals())


def message(request):
    articles = Article.objects.filter(status=BlogStatus.PUBLISHED)
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    links = Links.objects.all().order_by("-weights", "id")
    own_messages = OwnerMessage.objects.all()
    messages = Messages.objects.order_by('-id')
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    messages, total = paginate(messages, page_num=page_num, page_size=page_size)
    messages_num = Messages.objects.all()
    classification = Classification.class_list.get_classify_list()
    tag_cloud = json.dumps(Tag.tag_list.get_tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_article_by_date()
    return render(request, 'blog/message.html', locals())


def love(request):
    params = request.POST
    name = params['name']
    pw = params['pw']
    if name == 'maomao' and pw == 'nn':
        return render(request, 'blog/index1.html')
    else:
        return render(request, 'blog/404.htm')


@require_POST
def create_messages(request):
    params = request.POST
    name = params['name']
    email = params['email']
    messages = params['messages']
    Messages.create_message(
        name=name,
        email=email,
        content=messages
    )
    return render_json({'success': True, 'message': '留言成功！'})
