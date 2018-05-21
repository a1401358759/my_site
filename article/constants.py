# -*- coding: utf-8 -*-


class BlogStatus(object):
    DRAFT = 1
    PUBLISHED = 2

    CHOICES = (
        (DRAFT, u"草稿"),
        (PUBLISHED, u"已发布")
    )

    CHOICES_DICT = dict(CHOICES)
