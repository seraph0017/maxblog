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
            'name': ALL_WITH_RELATIONS,
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
            'id': ALL_WITH_RELATIONS,
            'author': ALL_WITH_RELATIONS,
            'title': ALL_WITH_RELATIONS,
            'belong_cate':ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }

    def build_filters(self,filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(ArticleResource, self).build_filters(filters)
        if 'author' in filters:
            author = filters['author']
            qset = models.Author.objects(name=author).first()
            orm_filters.update({'author__exact':qset})
        if 'belong_cate' in filters:
            belong_cate = filters['belong_cate']
            qset = models.Category.objects(name=belong_cate).first()
            orm_filters.update({'belong_cate__exact':qset})
        return orm_filters


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