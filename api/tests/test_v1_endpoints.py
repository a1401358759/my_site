from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from article.constants import BlogStatus, EditorKind
from article.models import Article, Author, Classification, Tag


class V1ApiTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Tester')
        self.classification = Classification.objects.create(name='Python')
        self.tag = Tag.objects.create(name='Django')

    def _create_article(self, title, publish_time, content='content', editor=EditorKind.Markdown):
        article = Article.objects.create(
            title=title,
            author=self.author,
            classification=self.classification,
            content=content,
            count=10,
            editor=editor,
            status=BlogStatus.PUBLISHED,
        )
        article.tags.add(self.tag)
        Article.objects.filter(pk=article.pk).update(
            publish_time=publish_time,
            last_update=publish_time,
        )
        article.refresh_from_db()
        return article

    def test_home_feed_supports_year_month_filter(self):
        april_article = self._create_article('April Post', datetime(2024, 4, 3, 12, 0, 0))
        self._create_article('May Post', datetime(2024, 5, 4, 12, 0, 0))

        response = self.client.get('/api/mysite/v1/home/', {
            'year': 2024,
            'month': 4,
            'page_size': 20,
        })

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        article_ids = [item['blog_id'] for item in payload['articles']]
        self.assertEqual(article_ids, [april_article.id])

    def test_home_feed_returns_raw_content_for_frontend_render(self):
        markdown_content = '### 标题\n\n```python\nprint("hi")\n```\n\n正文段落'
        article = self._create_article('Markdown Post', datetime(2024, 4, 10, 12, 0, 0), content=markdown_content)

        response = self.client.get('/api/mysite/v1/home/', {
            'page_size': 20,
        })

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        article_item = next(item for item in payload['articles'] if item['blog_id'] == article.id)
        self.assertIn('content', article_item)
        self.assertIn('editor', article_item)
        self.assertEqual(article_item['content'], markdown_content)
        self.assertEqual(article_item['editor'], EditorKind.Markdown)
        self.assertNotIn('summary_html', article_item)

    def test_archive_timeline_groups_articles_by_month(self):
        self._create_article('April Post', datetime(2024, 4, 10, 12, 0, 0))
        may_article = self._create_article('May Post', datetime(2024, 5, 8, 9, 30, 0))

        response = self.client.get('/api/mysite/v1/archive/')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertTrue(payload['archive_timeline'])
        latest_month = payload['archive_timeline'][0]
        self.assertEqual((latest_month['year'], latest_month['month']), (2024, 5))
        self.assertEqual(latest_month['article_count'], 1)
        self.assertEqual(latest_month['articles'][0]['blog_id'], may_article.id)
        self.assertIn('publish_day', latest_month['articles'][0])

    def test_article_detail_returns_raw_content_for_frontend_render(self):
        markdown_content = '### 标题\n\n```python\nprint("hello")\n```\n\n正文段落'
        article = self._create_article('Detail Markdown Post', datetime(2024, 4, 12, 12, 0, 0), content=markdown_content)

        response = self.client.get(f'/api/mysite/v1/articles/{article.id}/')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        self.assertIn('content', payload['article'])
        self.assertIn('editor', payload['article'])
        self.assertEqual(payload['article']['content'], markdown_content)
        self.assertEqual(payload['article']['editor'], EditorKind.Markdown)
        self.assertNotIn('content_html', payload['article'])

    def test_comments_v1_endpoint_supports_create_and_list(self):
        article = self._create_article('Comment Target', datetime(2024, 6, 1, 12, 0, 0))
        target = f'/articles/{article.id}'

        with patch('api.views.get_location_by_ip', return_value=('中国', '北京', '北京'), create=True), patch(
            'api.views.send_email_task', create=True
        ):
            create_response = self.client.post('/api/mysite/v1/comments/', {
                'nickname': '访客A',
                'email': 'guest@example.com',
                'website': 'https://example.com',
                'content': '这是第一条评论',
                'target': target,
            })

        self.assertEqual(create_response.status_code, 200)
        self.assertIn('application/json', create_response['Content-Type'])
        create_payload = create_response.json()
        self.assertEqual(create_payload['code'], 0)

        list_response = self.client.get('/api/mysite/v1/comments/', {
            'target': target,
            'page_num': 1,
            'page_size': 10,
        })

        self.assertEqual(list_response.status_code, 200)
        self.assertIn('application/json', list_response['Content-Type'])
        list_payload = list_response.json()
        self.assertEqual(list_payload['code'], 0)
        self.assertEqual(len(list_payload['comment_list']), 1)
        self.assertEqual(list_payload['comment_list'][0]['nickname'], '访客A')
