#!/usr/bin/env python
#encoding:utf-8
"""
crawler.autohome
~~~~~~~~~~~~~~~~~~~~
中奢网爬虫文件
"""
from gevent import monkey;monkey.patch_all()
from webanan.models import Site,Category,Author,Article,Domain,Keyword
# from maxblog.settings import redisClient
from utils.things import fetch_page, fetch_elements, get_log

from gevent.pool import Pool


# from multiprocessing import Pool

from datetime import datetime

# import redis
import lxml.html
import requests
# import math
import re



log = get_log(__file__)


# R = redis.StrictRedis()



class Server(object):
    """.. :py:class:: Server
    中奢网的爬虫Server
    """
    locate = {
        u'主机':(u'ul.pMenu>li>a',1,13),#返回list
        u'分类':(u'ul.pListTab>li>a',0,-1),#返回list
        u'最后一页':u'a.last',
        u'最后一页_特':(u'span.pages a',-2),
        u'文章节点':u'div.listDetail',#返回list

        u'标题':u'span.fb14d a',
        u'文章杂项':u'span.fb1220-bl',
        u'关键词':u'span.f1218-bl',
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
            log.info('already have site {}'.format(self.site_url))
            pass
        else:
            Site(name=self.site_name,url=self.site_url).save()
            log.info('site {} fetch done'.format(self.site_url))


    def get_domain(self):
        """.. :py:method::
        从site信息中获取domain信息,如果已经获取则pass
        """
        html = fetch_page(self.site_url)
        nodes = fetch_elements(html,u'主机',self.locate)
        site = Site.objects(url=self.site_url).first()
        for node in nodes:
            if Domain.objects(url = node.get(u'href')):
                log.info('already have domain {}'.format(node.get(u'href')))
                pass
            else:
                Domain(name=node.text,url=node.get(u'href'),belong_site=site).save()
                log.info('domain {} fetch done'.format(node.get(u'href')))

    def get_category(self):
        """.. :py:method::
        从domain信息中获取category信息,如果已经获取则pass
        """
        domains = Domain.objects().all()
        for domain in domains:
            html = fetch_page(domain.url)
            nodes = fetch_elements(html,u'分类',self.locate)
            domain = Domain.objects(url=domain.url).first()
            for node in nodes:
                if Category.objects(url=node.get(u'href')) or u'名车' in node.get(u'href'):
                    # print node.get(u'href')
                    log.info('already have category {}'.format(node.get(u'href').encode('utf-8')))
                    pass
                else:
                    Category(name=node.text,url=node.get(u'href'),belong_Domain=domain).save()
                    log.info('category {} fetch done'.format(node.get(u'href')))


    def get_article(self):
        """.. :py:method::
        从category信息中获取article和author信息,如果已经获取则pass
        """
        urls = self._get_all_pages()

        pool = Pool(size=50)
        for url in urls:
            pool.spawn(self._get_info, url)
        pool.join()


    
    def _get_info(self,url):
        """.. :py:method::
        从url中获取所有的信息
        """
        author = re.compile(r'')
        html = fetch_page(url[0])
        nodes = fetch_elements(html,u'文章节点',self.locate)
        for node in nodes:
            link_url = fetch_elements(node,u'标题',self.locate)[0].get('href')
            if Article.objects(url=link_url).first():
                log.info('already have article {}'.format(link_url))
                pass
            else:
                title = fetch_elements(node,u'标题',self.locate)[0].text
                sth = fetch_elements(node,u'文章杂项',self.locate)[0].text
                
                keyword = fetch_elements(node,u'关键词',self.locate)[0].text_content()
                category = url[1]
                key_list = []
                log.info('article {} fetch done'.format(link_url))
                author,date,keywords = self._get_details(sth, keyword)
                if author:
                    if Author.objects(name=author).first():
                        new_author = Author.objects(name=author).first()
                    else:
                        new_author = Author(name=author)
                        new_author.save()
                else:
                    new_author = None
                for key in keywords:
                    key_list.append(Keyword(name=key))
                new_article = Article(
                        title = title,
                        url = link_url,
                        publish_at = date,
                        author = new_author,
                        keywords = key_list,
                        belong_cate = category,
                    )
                new_article.save()

            



    def _get_details(self,sth,keyword):
        """.. :py:method::
        把sth和keyword解析成author,date和一个key数组
        """
        sth = sth.encode('utf-8')
        keywords = keyword.replace(u'关键词：',u'').strip().split(u' ')
        r_author = re.compile(r'文/?(\S*)')
        r_pub_date = re.compile(r'日期/?(\S*)')
        try:
            author = r_author.findall(sth)[0].decode('utf-8')
        except IndexError:
            author = None
        date = r_pub_date.findall(sth)[0].decode('utf-8')
        date_list = date.split(u'-')
        date = datetime(int(date_list[0]),int(date_list[1]),int(date_list[2]))

        return author,date,keywords






    def _get_all_pages(self):
        """.. :py:method::
        从category信息中获取所有list的url,返回一个list内容是所有页面的url地址
        """
        url_list = []
        categorys = Category.objects().all()
        for cate in categorys:
            html = fetch_page(cate.url)
            try:
                last_page_node = fetch_elements(html,u'最后一页',self.locate)[0]
                last_page_int = int(last_page_node.text.split(' ')[-1])
            except IndexError:
                try:
                    last_page_node = fetch_elements(html,u'最后一页_特',self.locate)[0]
                    last_page_int = int(last_page_node.text.split(' ')[-1])
                except IndexError:
                    last_page_int = 1
            for page in range(last_page_int):
                list_url = '{}list_{}.html'.format(cate.url,page)
                url_list.append((list_url,cate))
        return url_list








if __name__ == '__main__':


    from datetime import datetime
    start = datetime.now()
    server = Server()
    server.get_site()
    server.get_domain()
    server.get_category()
    server.get_article()
    stop = datetime.now()
    print stop - start




