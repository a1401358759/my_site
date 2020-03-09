# -*- coding: utf-8 -*-

import json
import random
import hashlib
from django.core.cache import cache
from article.models import Tag, Music, Article, Classification, Links, CarouselImg, Comments
from article.constants import BlogStatus

CACHE_TIME = 600  # second


def get_articles(key):
    articles = []
    if cache.get(key):
        articles = cache.get(key)
    else:
        articles = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by("-publish_time")
        if articles:
            cache.set(key, articles, None)
    return articles


def get_tags_and_musics(tag_key, music_key):
    color_array, music_list, tag_list = [
        '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
    ], [], []
    if cache.get(tag_key):
        tag_list = cache.get(tag_key)
    else:
        tag_list = list(Tag.objects.all())
        for tag in tag_list:
            tag.color = '#' + ''.join(random.sample(color_array, 6))  # 为每个标签随机生成颜色
        random.shuffle(tag_list)  # random.shuffle()的返回值是none，改变的是原来的元素
        if tag_list:
            cache.set(tag_key, tag_list, None)
    if cache.get(music_key):
        music_list = cache.get(music_key)
    else:
        musics = Music.objects.all()
        for item in musics:
            music_list.append({
                "name": item.name,
                "url": item.url,
                "cover": item.cover,
                "artist": item.artist,
                "lrc": item.lrc,
            })
        if music_list:
            random.shuffle(music_list)
            cache.set(music_key, json.dumps(music_list[:3]), CACHE_TIME)

    return tag_list, music_list


def get_popular_top10_blogs(key):
    new_post = []
    if cache.get(key):
        new_post = cache.get(key)
    else:
        new_post = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-count')[:8]
        if new_post:
            cache.set(key, list(new_post), 24 * 3600)  # 缓存24小时
    return new_post


def get_classifications(key):
    classification = []
    if cache.get(key):
        classification = cache.get(key)
    else:
        classification = Classification.class_list.get_classify_list()
        if classification:
            cache.set(key, classification, None)
    return classification


def get_date_list(key):
    date_list = []
    if cache.get(key):
        date_list = cache.get(key)
    else:
        date_list = Article.date_list.get_article_by_date()
        if date_list:
            cache.set(key, date_list, 24 * 3600)  # 缓存24小时
    return date_list


def get_archieve(key):
    archieve = []
    if cache.get(key):
        archieve = cache.get(key)
    else:
        archieve = Article.date_list.get_article_by_archive()
        if archieve:
            cache.set(key, archieve, 24 * 3600)  # 缓存24小时
    return archieve


def get_links(key):
    links = []
    if cache.get(key):
        links = cache.get(key)
    else:
        links = list(Links.objects.all())
        if links:
            cache.set(key, links, None)
    return links


def get_carousel_imgs(key, img_type):
    carouse_imgs = []
    if cache.get(key):
        carouse_imgs = cache.get(key)
    else:
        carouse_imgs = CarouselImg.objects.filter(img_type=img_type).order_by("-weights", "id")
        if carouse_imgs:
            cache.set(key, carouse_imgs, None)
    return carouse_imgs


def get_cache_comments(key):
    comments = []
    if cache.get(key):
        comments = cache.get(key)
    else:
        comments = Comments.objects.select_related().filter(target=key).order_by('-id')
        if comments:
            cache.set(key, comments, None)
    return comments


def gravatar_url(email, size=40):
    styles = ['identicon', 'monsterid', 'wavatar']
    url = 'https://www.gravatar.com/avatar/{}?s={}&d={}'.format(
        hashlib.md5(email.lower().encode("utf-8")).hexdigest(),
        size,
        random.choice(styles)
    )
    return url
