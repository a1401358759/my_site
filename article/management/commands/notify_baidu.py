# -*- coding: utf-8 -*-

import requests
from django.core.management.base import BaseCommand
from article.models import Article
from article.constants import BlogStatus, DOMAIN


class Command(BaseCommand):

    def notify_baidu(self):
        articles = Article.objects.filter(status=BlogStatus.PUBLISHED).order_by('-id')
        urls = [DOMAIN + article.get_absolute_url() for article in articles]
        api = 'http://data.zz.baidu.com/urls?site=yangsihan.com&token=7tNlHmCq6GVPoYfb'
        response = requests.post(api, data='\n'.join(urls))
        print (response.content.decode())

    def handle(self, *args, **options):
        self.notify_baidu()
