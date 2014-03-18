#!/usr/bin/env python
#encoding:utf-8
"""
api.webana
~~~~~~~~~~~~~~~~~~~~
网站分析模块的api方法
"""
from tastypie import authorization
from tastypie_mongoengine import resources
from webanan import models
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class SiteResource(resources.MongoEngineResource):
    """.. py:class::SiteResource
    Site模块的api定义方法
    """
    class Meta:
        queryset = models.Site.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
        resource_name = 'site'
        filtering = {
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


class ArticleResource(resources.MongoEngineResource):
    """.. py:class::ArticleResource
    Article模块的api定义方法
    """
    class Meta:
        queryset = models.Article.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
        resource_name = 'article'
        filtering = {
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


class DomainResource(resources.MongoEngineResource):
    """.. py:class::DomainResource
    Domain模块的api定义方法
    """
    class Meta:
        queryset = models.Domain.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
        resource_name = 'domain'
        filtering = {
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


class CategoryResource(resources.MongoEngineResource):
    """.. py:class::CategoryResource
    Category模块的api定义方法
    """
    class Meta:
        queryset = models.Category.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
        resource_name = 'category'
        filtering = {
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


class AuthorResource(resources.MongoEngineResource):
    """.. py:class::AuthorResource
    Author模块的api定义方法
    """
    class Meta:
        queryset = models.Author.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
        resource_name = 'author'
        filtering = {
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }