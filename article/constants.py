# -*- coding: utf-8 -*-


class BlogStatus(object):
    DRAFT = 1
    PUBLISHED = 2

    CHOICES = (
        (DRAFT, "草稿"),
        (PUBLISHED, "已发布")
    )

    CHOICES_DICT = dict(CHOICES)


class CarouselImgType(object):
    BANNER = 1
    ADS = 2

    CHOICES = (
        (BANNER, "banner"),
        (ADS, "ads")
    )

    CHOICES_DICT = dict(CHOICES)


class EditorKind(object):
    RichText = 1
    Markdown = 2

    CHOICES = (
        (RichText, "富文本编辑器"),
        (Markdown, "Markdown编辑器")
    )

    CHOICES_DICT = dict(CHOICES)


DOMAIN = 'https://yangsihan.com'
