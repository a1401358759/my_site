# -*- coding: utf-8 -*-

import random
import string
import markdown
from datetime import datetime
from django.core.cache import cache
from django.db.models import Q
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags

from utils.errorcode import ERRORCODE
from utils.common import form_error
from utils.dlibs.http.response import http_response
from utils.dlibs.tools.paginator import paginate
from utils.dlibs.tools.tools import get_clientip
from utils.libs.utils.lbs import get_location_by_ip
from config.common_conf import DOMAIN_NAME, BLOGGER_EMAIL
from utils.send_email import MailTemplate
from article.models import (
    Article, CarouselImg, Classification, Tag, Links, Visitor, Comments
)
from article.constants import BlogStatus, CarouselImgType, EditorKind
from article.backends import get_cache_comments, gravatar_url
from article.forms import CommentForm, GetCommentsForm
from article.tasks import send_email_task
from .forms import (
    BlogListForm, HomeFeedForm
)


def _serialize_article_list_item(article):
    content = article.content or ""
    summary = strip_tags(content) if article.editor == EditorKind.RichText else content
    summary = " ".join(summary.split())[:220]
    return {
        "blog_id": article.id,
        "title": article.title,
        "author": article.author.name,
        "classification": article.classification.name,
        "classification_id": article.classification_id,
        "tags": [item.name for item in article.tags.all()],
        "summary": summary,
        "content": content,
        "editor": article.editor,
        "publish_time": article.publish_time.strftime('%Y-%m-%d'),
        "last_update": article.last_update.strftime('%Y-%m-%d %H:%M'),
        "count": article.count,
    }


def _serialize_article_detail(article):
    return {
        "blog_id": article.id,
        "title": article.title,
        "author": {
            "name": article.author.name,
            "email": article.author.email,
            "website": article.author.website,
        },
        "classification": {
            "id": article.classification_id,
            "name": article.classification.name,
        },
        "tags": [{"id": item.id, "name": item.name} for item in article.tags.all()],
        "content": article.content,
        "publish_time": article.publish_time.strftime('%Y-%m-%d %H:%M'),
        "last_update": article.last_update.strftime('%Y-%m-%d %H:%M'),
        "count": article.count,
        "editor": article.editor,
        "status": article.status,
    }


def _serialize_nav_article(article):
    if not article:
        return None
    return {
        "blog_id": article.id,
        "title": article.title,
        "publish_time": article.publish_time.strftime('%Y-%m-%d')
    }


def _build_article_queryset(keyword="", tag="", classification="", year=None, month=None):
    query = Q(status=BlogStatus.PUBLISHED)
    if keyword:
        query &= (
            Q(title__icontains=keyword) |
            Q(classification__name__icontains=keyword) |
            Q(tags__name__icontains=keyword)
        )
    if tag:
        query &= Q(tags__name=tag)
    if classification:
        query &= Q(classification__name=classification)
    if year:
        query &= Q(publish_time__year=year)
    if month:
        query &= Q(publish_time__month=month)
    return Article.objects.select_related('author', 'classification').prefetch_related('tags').filter(query).distinct().order_by('-publish_time')


def _paginate_articles(article_queryset, page_num, page_size):
    if not article_queryset.exists():
        return [], 0, 0
    blogs, total = paginate(article_queryset, page_num, page_size, page_list=False)
    return list(blogs.object_list), total, blogs.paginator.num_pages


def blog_list(request):
    form = BlogListForm(request.GET)
    form.is_valid()

    title = (form.cleaned_data.get("title") or "").strip()
    page_num = form.cleaned_data.get('page_num') or 1
    page_size = form.cleaned_data.get('page_size') or 10

    blogs, total, total_pages = _paginate_articles(_build_article_queryset(keyword=title), page_num, page_size)
    blog_list = []
    for blog in blogs:
        blog_list.append({
            "blog_id": blog.id,
            "title": blog.title,
            "author": blog.author.name,
            "classification": blog.classification.name,
            "content": blog.content,
            "publish_time": blog.publish_time.strftime('%Y-%m-%d'),
            "count": blog.count
        })

    return http_response(request, statuscode=ERRORCODE.SUCCESS, context={
        "blog_list": blog_list,
        "total": total,
        "total_pages": total_pages,
        "page_num": page_num,
        "page_size": page_size,
    })


def get_banners(request):
    banners = CarouselImg.objects.filter(img_type=CarouselImgType.BANNER).order_by('-weights', 'id')
    banner_list = []
    for item in banners:
        banner_list.append({
            "img_url": item.path,
            "link_url": item.link,
            "name": item.name,
            "description": item.description,
        })

    context = {
        "banner_list": banner_list
    }
    return http_response(request, statuscode=ERRORCODE.SUCCESS, context=context)


def home_feed(request):
    form = HomeFeedForm(request.GET)
    form.is_valid()
    keyword = (form.cleaned_data.get('keyword') or '').strip()
    tag = (form.cleaned_data.get('tag') or '').strip()
    classification = (form.cleaned_data.get('classification') or '').strip()
    year = form.cleaned_data.get('year')
    month = form.cleaned_data.get('month')
    page_num = form.cleaned_data.get('page_num') or 1
    page_size = form.cleaned_data.get('page_size') or 8

    article_queryset = _build_article_queryset(
        keyword=keyword,
        tag=tag,
        classification=classification,
        year=year,
        month=month,
    )
    article_list, total, total_pages = _paginate_articles(article_queryset, page_num, page_size)

    popular_articles = Article.objects.select_related('author', 'classification').prefetch_related('tags').filter(
        status=BlogStatus.PUBLISHED
    ).order_by('-count', '-publish_time')[:6]
    classification_list = list(Classification.objects.annotate(
        article_count=Count('article', filter=Q(article__status=BlogStatus.PUBLISHED), distinct=True)
    ).values('id', 'name', 'article_count').order_by('-article_count', 'id'))
    tag_list = list(Tag.objects.annotate(
        article_count=Count('article', filter=Q(article__status=BlogStatus.PUBLISHED), distinct=True)
    ).filter(article_count__gt=0).values('id', 'name', 'article_count').order_by('-article_count', 'id'))

    archive_rows = Article.objects.filter(status=BlogStatus.PUBLISHED).annotate(
        month=TruncMonth('publish_time')
    ).values('month').annotate(article_count=Count('id')).order_by('-month')
    archive_list = []
    for item in archive_rows:
        archive_month = item['month']
        archive_list.append({
            "year": archive_month.year,
            "month": archive_month.month,
            "label": archive_month.strftime('%Y-%m'),
            "article_count": item['article_count'],
        })

    banner_list = list(CarouselImg.objects.filter(img_type=CarouselImgType.BANNER).order_by('-weights', 'id').values(
        'id', 'name', 'description', 'path', 'link', 'weights'
    ))
    ads_list = list(CarouselImg.objects.filter(img_type=CarouselImgType.ADS).order_by('-weights', 'id').values(
        'id', 'name', 'description', 'path', 'link', 'weights'
    ))
    link_list = list(Links.objects.order_by('-weights', 'id').values(
        'id', 'name', 'link', 'avatar', 'desc', 'email', 'weights'
    ))
    site_stats = Article.objects.filter(status=BlogStatus.PUBLISHED).aggregate(
        article_count=Count('id'),
        read_count=Sum('count'),
    )
    site_stats['read_count'] = site_stats.get('read_count') or 0

    return http_response(request, statuscode=ERRORCODE.SUCCESS, context={
        "filters": {
            "keyword": keyword,
            "tag": tag,
            "classification": classification,
            "year": year,
            "month": month,
        },
        "articles": [_serialize_article_list_item(item) for item in article_list],
        "popular_articles": [_serialize_article_list_item(item) for item in popular_articles],
        "classification_list": classification_list,
        "tag_list": tag_list,
        "archive_list": archive_list,
        "banner_list": banner_list,
        "ads_list": ads_list,
        "link_list": link_list,
        "site_stats": site_stats,
        "total": total,
        "total_pages": total_pages,
        "page_num": page_num,
        "page_size": page_size,
    })


def archive_timeline(request):
    archive_data = Article.date_list.get_article_by_archive()
    timeline = []
    for month_date, month_articles in archive_data.items():
        timeline.append({
            "year": month_date.year,
            "month": month_date.month,
            "label": month_date.strftime('%Y-%m'),
            "article_count": len(month_articles),
            "articles": [{
                "blog_id": item.id,
                "title": item.title,
                "publish_time": item.publish_time.strftime('%Y-%m-%d %H:%M'),
                "publish_day": item.publish_time.strftime('%m.%d'),
                "count": item.count,
            } for item in month_articles],
        })
    return http_response(request, statuscode=ERRORCODE.SUCCESS, context={
        "archive_timeline": timeline,
    })


def _safe_send_email(mail, mail_body):
    try:
        send_email_task.delay(mail, mail_body)
    except Exception:
        return


def comments_v1(request):
    if request.method == 'GET':
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
        comments = get_cache_comments(target)
        comments, total = paginate(comments, page_num, page_size)
        comment_list = []
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
                "parent_comment": md.convert(item.parent.content) if item.parent else '',
                "country": item.country,
                "province": item.province,
                "city": item.city,
            })

        return http_response(request, statuscode=ERRORCODE.SUCCESS, context={
            "comment_list": comment_list,
            "total": total,
            "page_num": page_num,
            "page_size": page_size,
        })

    if request.method == 'POST':
        form_data = request.POST if request.POST else request.parameters
        form = CommentForm(form_data)
        if not form.is_valid():
            return http_response(request, statuscode=ERRORCODE.PARAM_ERROR, msg_cn='</br>'.join(form_error(form)))

        nickname = form.cleaned_data.get('nickname')
        email = form.cleaned_data.get('email')
        website = form.cleaned_data.get('website')
        content = form.cleaned_data.get('content')
        target = form.cleaned_data.get('target')
        parent_comment_id = form.cleaned_data.get('parent_comment_id')

        try:
            ip_address = get_clientip(request)
            if cache.get(f'comment-rate:{ip_address}'):
                return http_response(request, statuscode=ERRORCODE.FAILED, msg_cn='您刚提交过评论，请稍后再提交！')

            user, _ = Visitor.objects.update_or_create(
                nickname=nickname,
                email=email,
                defaults={
                    "nickname": nickname,
                    "email": email,
                    "website": website,
                    "avatar": gravatar_url(email)
                }
            )
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

            if parent_comment_id:
                parent_comment = Comments.objects.select_related().filter(pk=parent_comment_id).first()
                reply_to = parent_comment.user if parent_comment else None
                comment_data.update({"parent_id": parent_comment_id, "reply_to": reply_to})
                if parent_comment and reply_to and reply_to.email:
                    mail_body = MailTemplate.notify_parent_user.format(
                        parent_user=parent_comment.user.nickname,
                        parent_comment=parent_comment.content,
                        comment_user=nickname,
                        comment=content,
                        target_url=DOMAIN_NAME + parent_comment.target,
                        anchor='#' + parent_comment.anchor
                    )
                    _safe_send_email(reply_to.email, mail_body)

            Comments.objects.create(**comment_data)

            if hasattr(cache, 'delete_pattern'):
                cache.delete_pattern(target)
            else:
                cache.delete(target)

            if not parent_comment_id and not user.blogger:
                mail_body = MailTemplate.notify_blogger.format(
                    nickname=nickname,
                    comment=content,
                    target_url=DOMAIN_NAME + target,
                    anchor='#' + anchor
                )
                _safe_send_email(BLOGGER_EMAIL, mail_body)

            cache.set(f'comment-rate:{ip_address}', str(datetime.now()), 60)
            return http_response(request, statuscode=ERRORCODE.SUCCESS)
        except Exception as exp:
            return http_response(request, statuscode=ERRORCODE.FAILED, msg=str(exp))

    return http_response(request, statuscode=ERRORCODE.PARAM_ERROR)


def article_detail(request, article_id):
    article = get_object_or_404(
        Article.objects.select_related('author', 'classification').prefetch_related('tags'),
        id=article_id,
        status=BlogStatus.PUBLISHED
    )

    previous_article = Article.objects.filter(status=BlogStatus.PUBLISHED, id__lt=article.id).order_by('-id').first()
    next_article = Article.objects.filter(status=BlogStatus.PUBLISHED, id__gt=article.id).order_by('id').first()
    related_articles = Article.objects.select_related('author', 'classification').prefetch_related('tags').filter(
        status=BlogStatus.PUBLISHED,
        classification_id=article.classification_id
    ).exclude(id=article.id).order_by('-publish_time')[:4]

    return http_response(request, statuscode=ERRORCODE.SUCCESS, context={
        "article": _serialize_article_detail(article),
        "previous_article": _serialize_nav_article(previous_article),
        "next_article": _serialize_nav_article(next_article),
        "related_articles": [_serialize_article_list_item(item) for item in related_articles],
        "not_update_days": (datetime.now() - article.last_update).days,
    })
