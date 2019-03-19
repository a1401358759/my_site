# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, InvalidPage


def paginator_page_list(number, page_range):
    """获得分页展示的页面范围

    number -- 当前页码
    """
    PAGE_SHOW = 7
    number = int(number)
    if len(page_range) <= PAGE_SHOW:
        return page_range
    else:
        if number <= 4:
            return page_range[0:PAGE_SHOW]
        elif (len(page_range) - number) < 4:
            return page_range[(len(page_range) - PAGE_SHOW):len(page_range)]
        else:
            return page_range[(number - 4):(number + 3)]


def paginate(info_list, page_num=1, page_size=10, page_list=True):
    """如果page_num超过最大页数，返回最后一页

    page_list - 返回页脚显示样式控制字段"""
    total = 0
    try:
        paginator = Paginator(info_list, page_size)
        total = paginator.count
        objects = paginator.page(page_num)
        if page_list:
            objects.page_list = paginator_page_list(page_num, [i for i in paginator.page_range])
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
        if page_list:
            objects.page_list = paginator_page_list(paginator.num_pages, paginator.page_range)

    return objects, total


def paginate_inc(info_list, page_num=1, page_size=10, page_list=True):
    """如果page_num超过最大页数，返回空列表[]

    page_list - 返回页脚显示样式控制字段"""
    total = 0
    try:
        paginator = Paginator(info_list, page_size)
        total = paginator.count
        objects = paginator.page(page_num)
        if page_list:
            objects.page_list = paginator_page_list(page_num, [i for i in paginator.page_range])
    except (EmptyPage, InvalidPage):
        objects = []

    return objects, total
