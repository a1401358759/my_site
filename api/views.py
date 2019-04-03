# -*- coding: utf-8 -*-

from django.db.models import Q
from utils.errorcode import ERRORCODE
from utils.dlibs.http.response import http_response
from utils.dlibs.tools.paginator import paginate
from article.models import (
    Article, CarouselImg
)
from article.constants import BlogStatus
from .forms import (
    BlogListForm
)


def blog_list(request):
    form = BlogListForm(request.GET)
    form.is_valid()
    query = Q(status=BlogStatus.PUBLISHED)

    title = form.cleaned_data.get("title")
    page_num = form.cleaned_data.get('page_num')
    page_size = form.cleaned_data.get('page_size')

    if title:
        query &= (Q(title__icontains=title) | Q(classification__name=title) | Q(tags__name=title))

    blogs = Article.objects.select_related().filter(query).order_by("-id")
    blogs, total = paginate(blogs, page_num, page_size)
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
        "page_num": page_num,
        "page_size": page_size,
    })


def get_banners(request):
    banners = CarouselImg.objects.order_by('id')
    banner_list = []
    for item in banners:
        banner_list.append({
            "img_url": item.path,
            "link_url": item.link
        })

    context = {
        "banner_list": banner_list
    }
    return http_response(request, statuscode=ERRORCODE.SUCCESS, context=context)
