"""CYP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import DetailView
from django.contrib import admin
from . import views
from News import models


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name = 'index'),
    url(r'^aboutUS/$', views.aboutUs, name = 'About'),
    url(r'^News/news_scroll_one.html$', views.news_scroll_one, name = 'news_scroll_one'),
    url(r'^News/news_scroll_two.html$', views.news_scroll_two, name = 'news_scroll_two'),
    url(r'^News/news_scroll_three.html$', views.news_scroll_three, name = 'news_scroll_three'),
    url(r'^recent_news/News/news_scroll.html$', views.news_scroll, name = 'news_scroll'),
    url(r'^house/News/republican_scroll.html$', views.republican_scroll, name = 'republican_scroll'),
    url(r'^senate/News/democrat_scroll.html$', views.democrat_scroll, name = 'democrat_scroll'),
    url(r'^recent_news/$', views.recent_news, name = 'recent_news'),
    url(r'^house/$', views.house, name = 'house'),
    url(r'^senate/$', views.senate, name = 'senate'),
    url(r'^splash_page/$', views.splash_page, name = 'splash_page'),
    url(r'^service.html$', views.service, name = 'serice'),
    # url(r'^(?P<pk>\d+)$', views.article, name = 'Article'),
    # url(r'^(?P<pk>\d+)$', DetailView.as_view(model=models.Articles, template_name='News/Article.html'))
    # url(r'^login/$', views.login, name = 'login'),
    #url(r'^accounts/login$', views.login, name = 'login'),
    #url(r'^accounts/auth$', views.auth_view, name = 'auth_view'),
    #url(r'^accounts/logout$', views.logout, name = 'logout'),
    #url(r'^accounts/loggedin$', views.loggedin, name = 'loggedin'),
    #url(r'^accounts/invalid$', views.invalid, name = 'invalid'),
    #url(r'^accounts/register$', views.UserFormView, name ='register')

]
