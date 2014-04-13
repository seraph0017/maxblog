#!/usr/bin/env python
#encoding:utf-8

from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
    url(r'^article/(?P<domain>\S+)/$',views.sec_list,name='sec_list'),
    url(r'^article/$',views.all_list,name='all_list'),
    url(r'^line/$',views.line_all_list,name='line_all'),
)