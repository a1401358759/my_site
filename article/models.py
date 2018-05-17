# coding: utf-8

from django.db import models
from collections import OrderedDict
from DjangoUeditor.models import UEditorField


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'姓名')
    email = models.EmailField(blank=True, verbose_name=u'邮件')
    website = models.URLField(blank=True, verbose_name=u'个人网站')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"文章作者"


class Messages(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'姓名')
    email = models.EmailField(max_length=30, verbose_name=u'邮箱')
    # content = UEditorField(max_length=200, verbose_name=u'留言', width=600,
    #                        imagePath="/static/media/", toolbars='full')
    content = models.TextField(verbose_name=u'留言', default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'留言时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"读者留言"

    @classmethod
    def create_message(cls, name, email, content):
        obj = Messages(
            name=name,
            email=email,
            content=content,
        )
        obj.save()
        return obj


class OwnerMessage(models.Model):
    # message = UEditorField(verbose_name=u'寄语', width=600,
    #                        imagePath="/static/media/", toolbars='full')

    message = models.TextField(verbose_name=u'寄语', default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return self.message

    class Meta:
        verbose_name_plural = u"主人寄语"


class TagManager(models.Manager):

    def get_tag_list(self):                 # 返回文章标签列表, 每个标签以及对应的文章数目
        tags = Tag.objects.all()
        tag_list = []
        for i in range(len(tags)):
            tag_list.append([])
        for i in range(len(tags)):
            temp = Tag.objects.get(name=tags[i])  # 获取当前标签
            posts = temp.article_set.all()      # 获取当前标签下的所有文章
            tag_list[i].append(tags[i].name)
            tag_list[i].append(len(posts))

        return tag_list


class Tag(models.Model):
    name = models.CharField(max_length=20, blank=True, verbose_name=u'标签名')
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    objects = models.Manager()
    tag_list = TagManager()

    @models.permalink
    def get_absolute_url(self):
        return('tagDetail', (),
               {'tag': self.name})

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"文章标签"


class ClassManager(models.Manager):

    @classmethod
    def get_classify_list(cls):  # 返回文章分类列表, 每个分类以及对应的文章数目
        classify = Classification.objects.all()  # 获取所有的分类
        classify_list = []
        for i in range(len(classify)):
            classify_list.append([])
        for i in range(len(classify)):
            temp = Classification.objects.get(name=classify[i])  # 获取当前分类
            posts = temp.article_set.all()  # 获取当前分类下的所有文章
            classify_list[i].append(classify[i])
            classify_list[i].append(len(posts))
        return classify_list


class Classification(models.Model):
    name = models.CharField(max_length=25)
    objects = models.Manager()  # 默认的管理器
    class_list = ClassManager()  # 自定义的管理器

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"文章分类"


class ArticleManager(models.Model):

    @classmethod
    def get_article_by_date(cls):  # 实现文章的按月归档, 返回 月份以及对应的文章数  如: [[2015.5,5],[2015.4,5]] ,
        post_date = Article.objects.dates('publish_time', 'month')
        post_date = post_date.reverse()  # 将post_date逆置,使之按月份递减的顺序排布
        date_list = []
        for i in range(len(post_date)):
            date_list.append([])
        for i in range(len(post_date)):
            current_year = post_date[i].year
            current_month = post_date[i].month
            temp_article = Article.objects.filter(publish_time__year=current_year, publish_time__month=current_month)
            temp_num = len(temp_article)
            date_list[i].append(post_date[i])
            date_list[i].append(temp_num)
        return date_list

    @classmethod
    def get_article_by_archive(cls):  # 返回一个字典,一个时间点,对应一个文章列表
        """

        :rtype: object
        """
        post_date = Article.objects.dates('publish_time', 'month')
        post_date = post_date.reverse()

        post_date_article = []
        for i in range(len(post_date)):
            post_date_article.append([])

        for i in range(len(post_date)):
            current_year = post_date[i].year
            current_month = post_date[i].month
            temp_article = Article.objects.filter(publish_time__year=current_year, publish_time__month=current_month)
            post_date_article[i] = temp_article

        dicts = OrderedDict()
        for i in range(len(post_date)):
            dicts.setdefault(post_date[i], post_date_article[i])
        return dicts


class Article(models.Model):  # 文章
    title = models.CharField(max_length=100, verbose_name=u'标题')
    author = models.ForeignKey(Author, verbose_name=u'作者')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签')  # 标签
    classification = models.ForeignKey(Classification, verbose_name=u'分类')  # 分类
    # content = UEditorField(blank=True, null=True, verbose_name=u'文章内容', width=600,
    #                        imagePath="/static/media/", toolbars='full')
    content = models.TextField(verbose_name=u'文章内容', default="")
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name=u'发表时间')
    count = models.IntegerField(default=0, verbose_name=u'文章点击数')  # 文章点击数,但未实现统计文章点击数的功能
    objects = models.Manager()  # 默认的管理器
    date_list = ArticleManager()  # 自定义的管理器

    @models.permalink
    def get_absolute_url(self):
        return ('detail', (), {
            'year': self.publish_time.year,
            'month': self.publish_time.strftime('%m'),
            'day': self.publish_time.strftime('%d'),
            'id': self.id
        })

    def get_tags(self):  # 返回一个文章对应的所有标签
        tag = self.tags.all()
        return tag

    def get_before_article(self):  # 返回当前文章的前一篇文章
        index = 0
        temp = Article.objects.order_by('id')
        cur = Article.objects.get(id=self.id)
        count = 0
        for i in temp:
            if i.id == cur.id:
                index = count
                break
            else:
                count += 1
        if index != 0:
            return temp[index - 1]

    def get_after_article(self):  # 返回当前文章的后一篇文章
        index = 0
        temp = Article.objects.order_by('id')
        max_num = len(temp) - 1
        cur = Article.objects.get(id=self.id)
        count = 0
        for i in temp:
            if i.id == cur.id:
                index = count
                break
            else:
                count += 1
        if index != max_num:
            return temp[index + 1]

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time']
        verbose_name_plural = u"文章"


class Links(models.Model):  # 友情链接
    name = models.CharField(max_length=50, verbose_name=u'链接名称')
    link = models.CharField(max_length=100, verbose_name=u'链接地址')
    weights = models.SmallIntegerField(default=10, verbose_name=u'权重', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"友情链接"
