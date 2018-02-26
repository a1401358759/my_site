# coding:utf-8
from django.shortcuts import render, HttpResponse
from article.models import Article, Tag, Classification, Messages, OwnerMessage
from django.http import Http404
from django.contrib.syndication.views import Feed  # 订阅RSS
import json
from django.views.decorators.http import require_POST


def render_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="text/json", status=status)


def home(request):
    is_home = True
    articles = Article.objects.all()
    # paginator = Paginator(articles, 5)  # 每个页面最多显示5篇文章
    # page_num = request.GET.get('page')
    # try:
    #     articles = paginator.page(page_num)
    # except PageNotAnInteger:
    #     articles = paginator.page(1)
    # except EmptyPage:
    #     articles = paginator.page(paginator.num_pages)

    # 显示最新发布的前5篇文章
    # ar_newpost = Article.objects.order_by('-publish_time')[:5]

    classification = Classification.class_list.get_Class_list()  # 分类,以及对应的数目
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()  # 按月归档,以及对应的文章数目

    return render(request, 'blog/index.html', locals())


def detail(request, year, month, day, id):
    try:
        article = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404

    # ar_newpost = Article.objects.order_by('-publish_time')[:5]

    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render(request, 'blog/content.html', locals())


def archive_month(request, year, month):
    is_arch_month = True
    articles = Article.objects.filter(publish_time__year=year).filter(publish_time__month=month)  # 当前日期下的文章列表
    # ar_newpost = Article.objects.order_by('-publish_time')[:5]
    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render(request, 'blog/index.html', locals())


def classfiDetail(request, classfi):
    is_classfi = True
    temp = Classification.objects.get(name=classfi)  # 获取全部的Article对象
    articles = temp.article_set.all()
    # ar_newpost = Article.objects.order_by('-publish_time')[:5]
    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render(request, 'blog/index.html', locals())


def tagDetail(request, tag):
    is_tag = True
    temp = Tag.objects.get(name=tag)  # 获取全部的Article对象
    # articles = Article.objects.filter(tags=tag)
    articles = temp.article_set.all()
    # ar_newpost = Article.objects.order_by('-publish_time')[:5]

    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render(request, 'blog/index.html', locals())


def about(request):
    # ar_newpost = Article.objects.order_by('-publish_time')[:5]
    articles = Article.objects.all()
    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render(request, 'blog/about.html', locals())


def archive(request):
    articles = Article.objects.all()
    archive = Article.date_list.get_Article_OnArchive()
    ar_newpost = Article.objects.order_by('-publish_time')[:5]
    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    return render(request, 'blog/archive.html', locals())


class RSSFeed(Feed):
    title = "RSS feed - Daniel的小站"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-publish_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.publish_time

    def item_description(self, item):
        return item.content


def blog_search(request):  # 实现对文章标题的搜索

    is_search = True
    # ar_newpost = Article.objects.order_by('-publish_time')[:5]
    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    error = False
    if 's' in request.POST:
        s = request.POST['s']
        if not s:
            return render(request, 'blog/index.html')
        else:
            articles = Article.objects.filter(title__icontains=s)
            if len(articles) == 0:
                error = True

    return render(request, 'blog/index.html', locals())


def message(request):
    articles = Article.objects.all()
    own_messages = OwnerMessage.objects.all()
    messages = Messages.objects.order_by('-created_at')
    messages_num = Messages.objects.all()
    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(), ensure_ascii=False)  # 标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    return render(request, 'blog/message.html', locals())


def love(request):
    params = request.POST
    name = params['name']
    pw = params['pw']
    if name == 'maomao' and pw == 'nn':
        return render(request, 'blog/index1.html')
    else:
        return render(request, 'blog/404.htm')


@require_POST
def create_messages(request):
    params = request.POST
    name = params['name']
    email = params['email']
    messages = params['messages']
    Messages.create_message(
        name=name,
        email=email,
        content=messages
    )
    return render_json({'success': True, 'message': '留言成功！'})
