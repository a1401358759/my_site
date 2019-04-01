# -*- coding: utf-8 -*-


class BlogStatus(object):
    DRAFT = 1
    PUBLISHED = 2

    CHOICES = (
        (DRAFT, u"草稿"),
        (PUBLISHED, u"已发布")
    )

    CHOICES_DICT = dict(CHOICES)


class CarouselImgType(object):
    BANNER = 1
    ADS = 2

    CHOICES = (
        (BANNER, u"banner"),
        (ADS, u"ads")
    )

    CHOICES_DICT = dict(CHOICES)


class EditorKind(object):
    RichText = 1
    Markdown = 2

    CHOICES = (
        (RichText, u"富文本编辑器"),
        (Markdown, u"Markdown编辑器")
    )

    CHOICES_DICT = dict(CHOICES)


DOMAIN = 'https://yangsihan.com'
