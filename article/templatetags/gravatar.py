# coding: utf-8

import hashlib
import random
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}


@register.filter
def gravatar_url(email, size=40):
    styles = ['identicon', 'monsterid', 'wavatar']
    url = 'https://www.gravatar.com/avatar/{}?s={}&d={}'.format(hashlib.md5(email.lower()).hexdigest(), size, random.choice(styles))
    return url

# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}


@register.filter
def gravatar(email, size=40):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
