#!/usr/bin/env python
#encoding:utf-8

from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',

    url(r'^$',views.admin_index,name='index'),
    url(r'^user/$',views.admin_user,name='user'),
    url(r'^user/(?P<user_id>\S+)/$',views.admin_user_del,name='user_del'),
    url(r'^site/$',views.admin_site,name='site'),
    url(r'^domain/$',views.admin_domain,name='domain'),
    url(r'^category/$',views.admin_category,name='category'),
    url(r'^article/$',views.admin_article,name='article'),
    url(r'^author/$',views.admin_author,name='author'),
)