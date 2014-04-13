#!/usr/bin/env python
#encoding:utf-8
"""
utils.things
~~~~~~~~~~~~~~~~~~~~
琐事定义基地
"""
from bson.objectid import ObjectId
from functools import wraps
from django.http import HttpResponse
from django.core.cache import cache

import lxml.html
import requests
import logging
import cPickle


def get_id():
    """.. :py:method::
    获取字符串的object-id
    """
    return str(ObjectId()) 



def fetch_page(url,timeout=30):
    """.. :py:method::
    封装http 加入智能等待 返回为lxml.html对象
    """
    try:
        page = requests.get(url,timeout=timeout)
    except:
        page = requests.get(url,timeout=timeout)
    html = lxml.html.fromstring(page.content)
    return html



def fetch_elements(html,lo_name,locate_source):
    """.. :py:method::
    根据对象库获取元素
    """
    path = locate_source[lo_name]
    if isinstance(path,tuple):
        if len(path) == 3:
            return html.cssselect(path[0])[path[1]:path[2]]
        elif len(path) == 2:
            return html.cssselect(path[0])[path[1]]
        else:
            raise Exception
    elif isinstance(path,basestring):
        return html.cssselect(path)
    else:
        raise Exception
    

def get_log(name):
    """.. :py:method::
    获取日志
    """
    r = logging.getLogger(name)
    r.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(name)s: %(message)s')
    ch.setFormatter(formatter)
    r.addHandler(ch)
    return r


def paginate(count=0, page=1, limit=20, **kwargs):
    """.. :py:method::
    提供分页方法
    """
    offset = (page - 1) * limit
    next_offset = offset + limit
    pages = [page]
    prev_page = page - 1
    next_page = page + 1
    prev_page_limit = kwargs.get('prev_page_limit', 3)
    next_page_limit = kwargs.get('next_page_limit', 3)
    total_page = (count / limit) + int(bool(count % limit))

    while prev_page and prev_page_limit:
        pages.append(prev_page)
        prev_page -= 1
        prev_page_limit -= 1

    while (next_page <= total_page) and next_page_limit:
        pages.append(next_page)
        next_page +=1
        next_page_limit -= 1

    pages.sort()
    paginator = {
        'count': count,
        'limit': limit,
        'current': page,
        'pages': pages,
        'offset':offset,
        'total_page':total_page,
        'next_offset': min(next_offset, count),
        'has_previous': bool(offset > 0),
        'has_next': bool(next_offset < count),
    }
    return paginator


def unauthed():
    """.. :py:method::
    验证失败的返回界面
    """
    response = HttpResponse("""<html><title>Auth required</title><body>
                            <h1>Authorization Required</h1></body></html>""", mimetype="text/html")
    response['WWW-Authenticate'] = 'Basic realm="Development"'
    response.status_code = 401
    return response

def http_basic_auth(func):
    """.. :py:method::
    后台登陆http基础验证
    """
    @wraps(func)
    def process_request(request, *args, **kwargs):
        if not request.META.has_key('HTTP_AUTHORIZATION'):
            return unauthed()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth) = authentication.split(' ',1)
            if 'basic' != authmeth.lower():
                return unauthed()
            auth = auth.strip().decode('base64')
            username, password = auth.split(':',1)
            if username == 'seraph' and password == 'x09083412':
                try:
                    return func(request, *args, **kwargs)
                except TypeError:
                    return func(request)
            return unauthed()
    return process_request


def mycache(timeout=30):
    """.. :py:method::
    重写了cache decroator,默认的timeout是30秒
    """
    def get_func(func):
        @wraps(func)
        def wrapper(*args,**kw):
            name_list = []
            for k,v in kw.iteritems():
                name_list.append(k)
                name_list.append(v)
            name = func.__name__
            name_list.append(name)
            fname = u'_'.join(name_list)
            mycache = cache.get(fname)
            if mycache:
                return cPickle.loads(mycache)
            else:
                cache.set(fname,cPickle.dumps(func(*args,**kw)),timeout=timeout)
                return func(*args,**kw)
        return wrapper
    return get_func




