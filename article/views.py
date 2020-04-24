# -*- coding: utf-8 -*-

import random
import string
import markdown
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db.models import Q, Count, Sum
from django.contrib.syndication.views import Feed  # 订阅RSS
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from utils.dlibs.tools.paginator import paginate
from utils.dlibs.http.response import render_json, http_response
from utils.dlibs.tools.tools import get_clientip
from utils.libs.utils.mine_qiniu import upload_data
from utils.libs.utils.lbs import get_location_by_ip
from utils.send_email import MailTemplate
from utils.errorcode import ERRORCODE
from config.common_conf import DOMAIN_NAME, BLOGGER_EMAIL
from article.models import Article, Classification, OwnerMessage, Tag, Visitor, Comments
from article.constants import BlogStatus, EditorKind, CarouselImgType
from article.backends import (
    get_tags_and_musics, get_popular_top10_blogs, get_links, gravatar_url,
    get_classifications, get_date_list, get_articles, get_archieve, get_carousel_imgs, get_cache_comments
)
from article.forms import CommentForm, GetCommentsForm
from article.tasks import send_email_task


@login_required
@csrf_exempt
@require_POST
def upload_file(request):
    """
    editor.md上传图片接口
    """
    filestream = request.FILES.get('editormd-image-file')
    if not filestream:
        return render_json({"success": 0, "message": "请选择文件", "url": ""})

    key, img_path = upload_data(filestream, 'blog')
    return render_json({"success": 1, "message": "上传成功", "url": img_path})


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
    carouse_imgs = get_carousel_imgs('tmp_carouse_imgs', CarouselImgType.BANNER)  # 轮播图
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
    return render(request, 'blog/index.html', locals())


def detail(request, year, month, day, id):
    """
    博客详情
    """
    try:
        article = Article.objects.get(id=id)
        # 文章阅读量统计，12小时内连续访问的IP只记录一次
        ip_address = get_clientip(request)
        key = ip_address + '_' + str(id)
        if cache.get(key) is None:
            article.count += 1
            article.save(update_fields=['count'])
            cache.set(key, str(datetime.now() + timedelta(hours=12)), 12 * 60 * 60)  # 设置12小时过期

        statics_count = Article.objects.aggregate(
            blog_count=Count('id', distinct=True),
            read_count=Sum('count'),
            tags_count=Count('tags', distinct=True)
        )
        # 生成文章目录
        if article.editor == EditorKind.Markdown:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.tables'
            ])
            article.content = md.convert(article.content)
            toc = md.toc
        tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
        not_update_days = (datetime.now() - article.last_update).days  # 计算文章距现在多长时间没有更新
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
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
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
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
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
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
    date_list = get_date_list('tmp_date_list')

    return render(request, 'blog/index.html', locals())


def about(request):
    """
    关于我
    """
    new_post = get_popular_top10_blogs('tmp_new_post')
    comments = get_cache_comments(request.path)
    page_num = request.GET.get("page") or 1
    comments, total = paginate(comments, page_num=page_num)
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
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
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
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
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
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
    own_message = random.sample(list(own_messages), 1)[0] if own_messages else ""  # 随机返回一个主人寄语
    date_list = get_date_list('tmp_date_list')
    classification = get_classifications('tmp_classification')
    new_post = get_popular_top10_blogs('tmp_new_post')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
    return render(request, 'blog/message.html', locals())


def love(request):
    from django.contrib.auth import authenticate

    name = request.POST.get('name')
    pw = request.POST.get('pw')
    user = authenticate(username=name, password=pw)
    if not user:
        return render(request, "blog/404.html")
    return render(request, "blog/love.html")


@require_GET
def my_resume(request):
    return render(request, 'resume/my_resume.html')


def links(request):
    """
    友情链接
    """
    links = get_links('tmp_links')
    random.shuffle(links)  # 友情链接随机排序
    new_post = get_popular_top10_blogs('tmp_new_post')
    classification = get_classifications('tmp_classification')
    tag_list, music_list = get_tags_and_musics('tmp_tags', 'tmp_musics')  # 获取所有标签，并随机赋予颜色
    ads_imgs = get_carousel_imgs('tmp_ads_imgs', CarouselImgType.ADS)  # 广告轮播图
    date_list = get_date_list('tmp_date_list')
    return render(request, 'blog/links.html', locals())


def add_comments_view(request):
    """
    添加评论
    """
    form = CommentForm(request.POST)
    if not form.is_valid():
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR)

    nickname = form.cleaned_data.get('nickname')
    email = form.cleaned_data.get('email')
    website = form.cleaned_data.get('website')
    content = form.cleaned_data.get('content')
    target = form.cleaned_data.get('target')
    parent_comment_id = form.cleaned_data.get('parent_comment_id')

    try:
        user, created = Visitor.objects.update_or_create(
            nickname=nickname,
            email=email,
            defaults={
                "nickname": nickname,
                "email": email,
                "website": website,
                "avatar": gravatar_url(email)
            }
        )
        ip_address = get_clientip(request)
        country, province, city = get_location_by_ip(ip_address)
        anchor = ''.join(random.sample(string.ascii_lowercase + string.digits, 16))
        comment_data = {
            "user_id": user.id,
            "content": content,
            "target": target,
            "ip_address": ip_address,
            "country": country,
            "province": province,
            "city": city,
            "anchor": anchor,
        }
        # 二级回复
        if parent_comment_id:
            parent_comment = Comments.objects.select_related().filter(pk=parent_comment_id).first()
            reply_to = parent_comment.user if parent_comment else None
            comment_data.update({"parent_id": parent_comment_id, "reply_to": reply_to})
            mail_body = MailTemplate.notify_parent_user.format(
                parent_user=parent_comment.user.nickname,
                parent_comment=parent_comment.content,
                comment_user=nickname,
                comment=content,
                target_url=DOMAIN_NAME + parent_comment.target,
                anchor='#' + parent_comment.anchor
            )
            send_email_task.delay(reply_to.email, mail_body)
        Comments.objects.create(**comment_data)
        cache.delete_pattern(target)  # 清除缓存
        if not parent_comment_id and not user.blogger:
            mail_body = MailTemplate.notify_blogger.format(
                nickname=nickname,
                comment=content,
                target_url=DOMAIN_NAME + target,
                anchor='#' + anchor
            )
            send_email_task.delay(BLOGGER_EMAIL, mail_body)
        return http_response(request, statuscode=ERRORCODE.SUCCESS)
    except Exception as exp:
        return http_response(request, statuscode=ERRORCODE.FAILED, msg=exp)


def get_comments_view(request):
    """
    获取评论列表
    """
    form = GetCommentsForm(request.GET)
    if not form.is_valid():
        return http_response(request, statuscode=ERRORCODE.PARAM_ERROR)

    page_num = form.cleaned_data.get('page_num') or 1
    page_size = form.cleaned_data.get('page_size') or 10
    target = form.cleaned_data.get('target')

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    comment_list = []
    comments = get_cache_comments(target)
    comments, total = paginate(comments, page_num, page_size)
    for item in comments:
        comment_list.append({
            "comment_id": item.id,
            "anchor": item.anchor,
            "comment": md.convert(item.content),
            "avatar": item.user.avatar,
            "website": item.user.website,
            "nickname": item.user.nickname,
            "blogger": True if item.user.blogger else False,
            "created_time": item.created_time.strftime("%Y-%m-%d %H:%M"),
            "reply_to": True if item.reply_to else False,
            "reply_to_user": item.reply_to.nickname if item.reply_to else '',
            "parent_anchor": item.parent.anchor if item.parent else '',
            "parent_comment": md.convert(item.parent.content) if item.parent else ''
        })

    return http_response(request, statuscode=ERRORCODE.SUCCESS, context={
        "comment_list": comment_list,
        "total": total,
        "page_num": page_num,
        "page_size": page_size,
    })


def page_not_found(request, exception):
    return render(request, 'blog/404.html')
