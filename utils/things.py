#!/usr/bin/env python
#encoding:utf-8
"""
utils.things
~~~~~~~~~~~~~~~~~~~~
琐事定义基地
"""
from bson.objectid import ObjectId
import lxml.html
import requests

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
    
