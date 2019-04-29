# -*- coding: utf-8 -*-

import random
from django.db.models import Q, Count, Sum
from django.contrib.syndication.views import Feed  # 订阅RSS
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from utils.dlibs.tools.paginator import paginate
from utils.dlibs.http.response import render_json
from utils.libs.utils.mine_qiniu import upload_data
from .models import Article, Classification, OwnerMessage, Tag
from .constants import BlogStatus
from .backends import (get_tags_and_musics, get_popular_top10_blogs, get_links,
                       get_classifications, get_date_list, get_articles, get_archieve, get_carousel_imgs
                       )
from .tasks import submit_urls_to_baidu


@login_required
@csrf_exempt
@require_POST
def upload_file(request):
    """
    editor.md上传图片接口
    """
    filestream = request.FILES.get('editormd-image-file')
    if not filestream:
        return render_json({"success": 0, "message": u"请选择文件", "url": ""})

    key, img_path = upload_data(filestream, 'blog')
    return render_json({"success": 1, "message": u"上传成功", "url": img_path})


@login_required
@csrf_exempt
@require_POST
def upload_rich_file(request):
    """
    wangEditor上传图片接口, 支持批量上传
    """
    files = request.FILES
    if not files:
        return render_json({"errno": 1, "data": []})

    img_path_list = []
    for item in files:
        key, img_path = upload_data(files.get(item), 'blog')
        img_path_list.append(img_path)

    return render_json({"errno": 0, "data": img_path_list})


def home(request):
    """
    博客首页
    """
    is_home = True
    articles = get_articles('tmp_articles')
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    new_post = get_popular_top10_blogs('tmp_new_post')  # 阅读量最高的十篇文章
    classification = get_classifications('tmp_classification')  # 分类,以及对应的数目
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')  # 按月归档,以及对应的文章数目
    carouse_imgs = get_carousel_imgs('tmp_carouse_imgs')  # 轮播图
    submit_urls_to_baidu.delay()
    return render(request, 'blog/index.html', locals())


def detail(request, year, month, day, id):
    """
    博客详情
    """
    try:
        article = Article.objects.get(id=id)
        article.count += 1
        article.save(update_fields=['count'])
        statis_count = Article.objects.aggregate(
            blog_count=Count('id'),
            read_count=Sum('count'),
            tags_count=Count('tags', distinct=True)
        )
        tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
        return render(request, 'blog/content.html', locals())
    except Article.DoesNotExist:
        raise Http404


def archive_month(request, year, month):
    is_arch_month = True

    articles = Article.objects.filter(publish_time__year=year, publish_time__month=month, status=BlogStatus.PUBLISHED)  # 当前日期下的文章列表
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')

    return render(request, 'blog/index.html', locals())


def classfiDetail(request, classfi):
    """
    按分类查找
    """
    is_classfi, articles, total = True, [], 0
    temp = Classification.objects.filter(name__icontains=classfi).first()
    if temp:
        articles = temp.article_set.filter(status=BlogStatus.PUBLISHED)
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')

    return render(request, 'blog/index.html', locals())


def tagDetail(request, tag):
    is_tag, articles, total = True, [], 0
    temp = Tag.objects.filter(name=tag).first()
    if temp:
        articles = temp.article_set.filter(status=BlogStatus.PUBLISHED)
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)

    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')

    return render(request, 'blog/index.html', locals())


def about(request):
    """
    关于我
    """
    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')

    return render(request, 'blog/about.html', locals())


def archive(request):
    """
    文章归档
    """
    archive = get_archieve('tmp_archive')
    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')

    return render(request, 'blog/archive.html', locals())


class RSSFeed(Feed):
    title = "RSS feed - 杨学峰博客"
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


def blog_search(request):
    """
    实现对文章标题，标签，分类的搜索
    """
    is_search = True
    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')
    error = False

    query = Q()
    s = request.GET.get('s') or ""
    if s:
        query &= (Q(title__icontains=s) | Q(classification__name=s) | Q(tags__name=s))

    articles = Article.objects.filter(query)
    page_num = request.GET.get("page") or 1
    page_size = request.GET.get("page_size") or 5
    articles, total = paginate(articles, page_num=page_num, page_size=page_size)
    if total == 0:
        error = True

    return render(request, 'blog/index.html', locals())


def message(request):
    """
    主人寄语
    """
    own_messages = OwnerMessage.objects.all()
    own_message = random.sample(own_messages, 1)[0] if own_messages else ""  # 随机返回一个主人寄语
    date_list = get_date_list('tmp_date_list')
    classification = get_classifications('tmp_classification')
    new_post = get_popular_top10_blogs('tmp_new_post')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    return render(request, 'blog/message.html', locals())


def love(request):
    name = request.POST.get('name')
    pw = request.POST.get('pw')
    if name == 'maomao' and pw == 'nn':
        return render(request, 'blog/love.html')
    else:
        return render(request, 'blog/404.html')


@require_GET
def my_resume(request):
    return render(request, 'resume/my_resume.html')


def links(request):
    """
    友情链接
    """
    links = get_links('links')
    random.shuffle(links)  # 友情链接随机排序
    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    date_list = get_date_list('tmp_date_list')
    return render(request, 'blog/links.html', locals())
