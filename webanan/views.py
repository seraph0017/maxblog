#!/usr/bin/env python
#encoding:utf-8
"""
webanan.views
~~~~~~~~~~~~~~~~~~~~
琐事定义基地
"""
from django.http import Http404
from django.shortcuts import render_to_response, RequestContext
from models import Article, Category, Domain
from collections import OrderedDict
from utils.things import mycache


@mycache(timeout=30)
def all_list(request):
    """.. :py:method::
    webanan的主页views方法
    """
    domains_list = []
    domain_list = Domain.objects().all()
    for do in domain_list:
        domains_list.append(do.name)
    title = u'各主机文章数量'
    per_dict = {}
    domains = Domain.objects().all()
    article_all = Article.objects().count()
    for domain in domains:
        categories = Category.objects(belong_Domain=domain).all()
        domain_count = 0
        
        for cate in categories:
            article_num = Article.objects(belong_cate=cate).count()
            domain_count = domain_count + article_num
        per_dict[domain.name] = float(u"%.2f" % (float(domain_count)/article_all))
    per_dict = OrderedDict(sorted(per_dict.items(), key=lambda t: t[1]))
    return render_to_response('webanan_list.html',{
        'title': title,
        'per_dict':per_dict,
        'domains':domains_list,
        })


@mycache(timeout=30)
def sec_list(request,domain=None):
    """.. :py:method::
    webanan的各下属分类的views方法
    """
    domains_list = []
    domain_list = Domain.objects().all()
    for do in domain_list:
        domains_list.append(do.name)
    title = u'{}分类文章数量'.format(domain)
    per_dict = {}
    domain_obj = Domain.objects(name=domain).first()
    if domain_obj:
        categories = Category.objects(belong_Domain=domain_obj).all()
        article_all = 0
        for cate in categories:
            article_all = article_all + Article.objects(belong_cate=cate).count()
        for cate in categories:
            article_num = Article.objects(belong_cate=cate).count()
            per_dict[cate.name] = float(u"%.2f" % (float(article_num)/article_all))
        per_dict = OrderedDict(sorted(per_dict.items(), key=lambda t: t[1]))
    else:
        raise Http404
    return render_to_response('webanan_list.html',{
                'title': title,
                'per_dict':per_dict,
                'domains':domains_list,
                })



def line_all_list(request):
    return render_to_response('webanan_line.html',{
                'title': 'title',
                'per_dict':'haha',
                'domains':'domains_list',
                })

