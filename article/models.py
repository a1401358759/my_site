# coding:utf-8
from django.db import models
from django.core.urlresolvers import reverse
from collections import OrderedDict
from DjangoUeditor.models import UEditorField


class Author(models.Model):
    name = models.CharField(max_length=30, verbose_name='姓名')
    email = models.EmailField(blank=True, verbose_name='邮件')
    website = models.URLField(blank=True, verbose_name='个人网站')

    def __unicode__(self):
        return self.name


class Messages(models.Model):
    name = models.CharField(max_length=30, verbose_name='姓名')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    content = UEditorField(max_length=200, verbose_name='留言', width=600,
                           imagePath="/static/media/", toolbars='full')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')

    def __unicode__(self):
        return self.name

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
    message = UEditorField(verbose_name='寄语', width=600,
                           imagePath="/static/media/", toolbars='full')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.message


class TagManager(models.Manager):
    def get_Tag_list(self):                 # 返回文章标签列表, 每个标签以及对应的文章数目
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
    name = models.CharField(max_length=20, blank=True, verbose_name='标签名')
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    objects = models.Manager()
    tag_list = TagManager()

    @models.permalink
    def get_absolute_url(self):
        return('tagDetail', (),
               {'tag': self.name})

    def __unicode__(self):
        return self.name


class ClassManager(models.Manager):
    def get_Class_list(self):  # 返回文章分类列表, 每个分类以及对应的文章数目
        classf = Classification.objects.all()  # 获取所有的分类
        class_list = []
        for i in range(len(classf)):
            class_list.append([])
        for i in range(len(classf)):
            temp = Classification.objects.get(name=classf[i])  # 获取当前分类
            posts = temp.article_set.all()  # 获取当前分类下的所有文章
            class_list[i].append(classf[i])
            class_list[i].append(len(posts))
        return class_list


class Classification(models.Model):
    name = models.CharField(max_length=25)
    objects = models.Manager()  # 默认的管理器
    class_list = ClassManager()  # 自定义的管理器
      
    def __unicode__(self):
        return self.name


class ArticleManager(models.Model):
    def get_Article_onDate(self):  # 实现文章的按月归档, 返回 月份以及对应的文章数  如: [[2015.5,5],[2015.4,5]] ,
        post_date = Article.objects.dates('publish_time', 'month')
        # post_date = post_date.reverse() # 将post_date逆置,使之按月份递减的顺序排布
        date_list = []
        for i in range(len(post_date)):
            date_list.append([])
        for i in range(len(post_date)):
            curyear = post_date[i].year
            curmonth = post_date[i].month
            tempArticle = Article.objects.filter(publish_time__year=curyear).filter(publish_time__month=curmonth)
            tempNum = len(tempArticle)
            date_list[i].append(post_date[i])
            date_list[i].append(tempNum)
        return date_list

    def get_Article_OnArchive(self):  # 返回一个字典,一个时间点,对应一个文章列表
        post_date = Article.objects.dates('publish_time', 'month')
        # post_date = post_date.reverse()

        post_date_article = []
        for i in range(len(post_date)):
            post_date_article.append([])

        for i in range(len(post_date)):
            curyear = post_date[i].year
            curmonth = post_date[i].month
            tempArticle = Article.objects.filter(publish_time__year=curyear).filter(publish_time__month=curmonth)
            post_date_article[i] = tempArticle
      
        dicts = OrderedDict()
        for i in range(len(post_date)):
            dicts.setdefault(post_date[i], post_date_article[i])
        return dicts


class Article(models.Model):  # 文章
    title = models.CharField(max_length=100, verbose_name='标题')
    author = models.ForeignKey(Author, verbose_name='作者')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')  # 标签
    classification = models.ForeignKey(Classification, verbose_name='分类')  # 分类
    content = UEditorField(blank=True, null=True, verbose_name='文章内容', width=600,
                           imagePath="/static/media/", toolbars='full')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')
    count = models.IntegerField(default=0, verbose_name='文章点击数')  # 文章点击数,但未实现统计文章点击数的功能
    objects = models.Manager()  # 默认的管理器
    date_list = ArticleManager()  # 自定义的管理器
  
    @models.permalink
    def get_absolute_url(self):
        return ('detail', (), {
           'year': self.publish_time.year,
           'month': self.publish_time.strftime('%m'),
           'day': self.publish_time.strftime('%d'),
           'id': self.id})
     
    def get_tags(self):  # 返回一个文章对应的所有标签
        tag = self.tags.all()
        return tag
           
    def get_before_article(self):  # 返回当前文章的前一篇文章
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
            return temp[index-1]

    def get_after_article(self):  # 返回当前文章的后一篇文章
        temp = Article.objects.order_by('id')
        max = len(temp)-1
        cur = Article.objects.get(id=self.id)
        count=0
        for i in temp:
            if i.id == cur.id:
                index = count
                break
            else:
                count += 1
        if index != max:
            return temp[index+1]

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time']


      


