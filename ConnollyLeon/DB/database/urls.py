"""DB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from apscheduler.scheduler import Scheduler
from . import views
from .tests import *

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^user/$', views.postuser, name='user'),
    url(r'^goods/status/(?P<status>[0-9]+)/$', views.goodsstatus, name='goodsstatus'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^user/(?P<pk>[\w]+)/$', views.user, name='money'),
    url(r'^goods/(?P<pk>[0-9]+)/$', views.goods, name='goods'),
    url(r'^goods/$', views.postgoods, name='postgoods')
]

# sched = Scheduler()


# @sched.interval_schedule(seconds=10)
# def my_task():
#    refresh_memcache()


# sched.start()
