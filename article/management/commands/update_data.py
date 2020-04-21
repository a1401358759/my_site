# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from article.models import Article


class Command(BaseCommand):

    def update_data(self):
        count = 0
        articles = Article.objects.all()
        for article in articles:
            article.last_update = article.publish_time
            article.save(update_fields=['last_update'])
            count += 1
        print('刷新完成，共更新%d条数据。' % count)

    def handle(self, *args, **options):
        self.update_data()
