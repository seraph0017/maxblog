#!/usr/bin/env python
#encoding:utf-8
"""
crawler.autohome
~~~~~~~~~~~~~~~~~~~~
中奢网爬虫文件
"""
from webana.models import Site,Category,Author,Article,Domain
# from maxblog.settings import redisClient
from utils.things import fetch_page, fetch_elements

import lxml.html
import requests






class Server(object):
    """.. :py:class:: Server
    中奢网的爬虫Server
    """
    locate = {
        u'主机':(u'ul.pMenu>li>a',1,13),#返回list
    }

    def __init__(self):
        self.site_url = u'http://www.chinaluxus.com/'
        self.site_name = u'中奢网'




    def get_site(self):
        """.. :py:method::
        获取site信息，如果已经获取则pass
        """
        site_instance = Site.objects(url=self.site_url).first()
        if site_instance:
            pass
        else:
            Site(name=self.site_name,url=self.site_url).save()


    def get_domain(self):
        """.. :py:method::
        从site信息中获取domain信息,如果已经获取则pass
        """
        html = fetch_page(self.site_url)
        nodes = fetch_elements(html,u'主机',self.locate)
        site = Site.objects(url=self.site_url).first()
        for node in nodes:
            if Domain.objects(url = node.get(u'href')):
                pass
            else:
                Domain(name=node.text,url=node.get(u'href'),belong_site=site).save()

    def get_category(self):
        """.. :py:method::
        从domain信息中获取category信息,如果已经获取则pass
        """



if __name__ == '__main__':
    server = Server()
    server.get_site()
    server.get_domain()



