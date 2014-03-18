#!/usr/bin/env python
#encoding:utf-8
"""
webana.models
~~~~~~~~~~~~~~~~~~~~
网站分析模块的models文件 定义所有的模型
"""
from mongoengine import *
from utils.things import get_id
from datetime import datetime
# from maxblog.settings import connect

class Site(Document):
    """.. :py:class:: Site
    网站模型
    """
    id = StringField(primary_key=True, default=get_id)
    name = StringField()
    url = URLField(required=True)
    create_at = DateTimeField(default=datetime.utcnow())

    meta = {
        'indexes':['url']
    }

    def __unicode__(self):
        return self.name



class Domain(Document):
    """.. :py:class:: Domain
    主机名，算是更上一级分类
    """
    id = StringField(primary_key=True, default=get_id)
    name = StringField()
    url = URLField(required=True)
    create_at = DateTimeField(default=datetime.utcnow())
    belong_site = ReferenceField(Site)
    meta = {
        'indexes':['name','url']
    }
    def __unicode__(self):
        return self.name



class Category(Document):
    """.. :py:class:: Category
    类别目录模型
    """
    id = StringField(primary_key=True, default=get_id)
    name = StringField()
    url = URLField(required=True)
    create_at = DateTimeField(default=datetime.utcnow())
    belong_Domain = ReferenceField(Domain)
    meta = {
        'indexes':['name']
    }
    def __unicode__(self):
        return self.name


class Author(Document):
    """.. :py:class:: Author
    作者
    """
    id = StringField(primary_key=True, default=get_id)
    name = StringField()
    create_at = DateTimeField(default=datetime.utcnow())
    meta = {
        'indexes':['name']
    }
    def __unicode__(self):
        return self.name



class Keyword(EmbeddedDocument):
    """.. :py:class:: Keyword
    关键字模型
    """
    name = StringField()
    def __unicode__(self):
        return self.name



class Article(Document):
    """.. :py:class:: Article
    文章模型
    """
    id = StringField(primary_key=True, default=get_id)
    title = StringField()
    url = URLField(required=True)
    create_at = DateTimeField(default=datetime.utcnow())
    publish_at = DateTimeField()
    author = ReferenceField(Author)
    keywords = ListField(EmbeddedDocumentField(Keyword))
    belong_cate = ReferenceField(Category)

    meta = {
        'indexes':['title','author','belong_cate']
    }
    def __unicode__(self):
        return self.title


