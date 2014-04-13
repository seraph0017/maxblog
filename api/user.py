#!/usr/bin/env python
#encoding:utf-8
"""
api.user
~~~~~~~~~~~~~~~~~~~~
用户模块的api方法
"""
from tastypie import authorization
from tastypie_mongoengine import resources
from accounts import models
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class UserResource(resources.MongoEngineResource):
    """.. py:class::UserResource
    user模块的api定义方法
    """
    class Meta:
        queryset = models.User.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        excludes = ['password']
        authorization = authorization.Authorization()
        resource_name = 'user'

        filtering = {
            'username': ALL_WITH_RELATIONS,
            'email': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


