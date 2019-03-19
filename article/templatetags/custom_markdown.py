# coding:utf-8

import markdown
import mistune
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    return mark_safe(markdown.markdown(
        value, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables'
        ],
        safe_mode=True,
        enable_attributes=False)
    )


@register.filter(is_safe=True)  # 注册template filter
def markdown_to_html(value):
    markdown = mistune.Markdown()
    return mark_safe(markdown(value))
