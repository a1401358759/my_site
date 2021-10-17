# coding:utf-8

# from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from article import views


urlpatterns = [
    # url('admin/', include(admin.site.urls)),
    path('manager/', include("manager.urls")),
    path('api/mysite/', include("api.urls")),
    path('', views.home, name="home"),  # 主页
    path('about/', views.about, name="about"),  # 关于我
    path('message/', views.message, name="message"),  # 留言
    path('links/', views.links, name="links"),  # 友情链接
    path('archive/', views.archive, name="archive"),  # 归档
    path('feed/', views.RSSFeed(), name="RSS"),  # rss订阅
    path('search/', views.blog_search, name="search"),  # 按文章标题搜索
    path('article/<int:year>/<int:month>/<int:day>/<int:id>/', views.detail, name="detail"),  # 每篇文章
    path('article/<int:year>/<int:month>/', views.archive_month, name="archive_month"),  # 按月归档
    path('articleClassfi/<str:classfi>/', views.classfiDetail, name="classfiDetail"),  # 每个分类页下面的文章
    path('articleTag/<str:tag>/', views.tagDetail, name="tagDetail"),  # 每个标签页下面的文章
    path('love/', views.love),
    path('my-resume/', views.my_resume, name='my_resume'),  # 简历
    path('tools/', views.tool_box, name='tool_box'),  # 工具
    path('upload/', views.upload_file, name='upload_file'),
    path('upload-rich/', views.upload_rich_file, name='upload_rich_file'),
    path('add-comments/', views.add_comments_view, name='add_comments'),
    path('get-comments/', views.get_comments_view, name='get_comments'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler404 = views.page_not_found
