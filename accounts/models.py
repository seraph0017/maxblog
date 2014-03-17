#!/usr/bin/env python
#encoding:utf-8
"""
accounts.models
~~~~~~~~~~~~~~~~~~~~
用户模块的models文件 定义所有的模型
"""
from mongoengine import *
from mongoengine.django.auth import User
from utils.things import get_id



class User(User):
    """.. :py:class:: User
    用户模块
    """
    id = StringField(primary_key=True, default=get_id)
    email = EmailField(required=True)
    username = StringField(max_length=50,min_length=1)
    password = StringField(max_length=500,min_length=6)

    meta = {
        'indexes':['email','username']
    }

    @classmethod
    def create_user(cls,email=None,username=None,password=None,**kw):
        """.. :py:method::
        自己重写create_user方法
        """
        new_user = super(User,cls).create_user(email=email,username=username,password=password)
        for k,v in kw.iteritems():
            setattr(new_user,k,v)
        new_user.save()
        return new_user



    def __unicode__(self):
        return self.username









