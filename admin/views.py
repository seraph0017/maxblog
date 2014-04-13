#!/usr/bin/env python
#encoding:utf-8
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect

from webanan import models as web_model
from accounts import models as acc_model
from utils.things import paginate, http_basic_auth


import json



@http_basic_auth
def admin_index(request):
    user_count = acc_model.User.objects().count()
    site_count = web_model.Site.objects().count()
    domain_count = web_model.Domain.objects().count()
    category_count = web_model.Category.objects().count()
    author_count = web_model.Author.objects().count()
    article_count = web_model.Article.objects().count()
    list_dict = {
        u'用户总数':user_count,
        u'网站总数':site_count,
        u'主机总数':domain_count,
        u'类别总数':category_count,
        u'作者总数':author_count,
        u'文章总数':article_count,
    }
    return render_to_response(
        u'admin_main.html',
        {
        u'list_dict':list_dict,
        })


@csrf_protect
def admin_user(request):
    if request.method == u'GET':
        bread = u'用户'
        info_list = acc_model.User.objects().all()
        info_head = [u'用户名',u'邮箱',u'操作']
        return render_to_response(
            u'admin_user.html',
            {
            u'bread':bread,
            u'info_head':info_head,
            u'info_list':info_list,
            })
    elif request.method == u'POST':
        username = request.POST[u'username'] if u'username' in request.POST else None
        password = request.POST[u'password'] if u'password' in request.POST else None
        email    = request.POST[u'email'] if u'email' in request.POST else None
        if username and password and email:
            acc_model.User.create_user(email=email,username=username,password=password)
            return HttpResponse(json.dumps({
                        'status':'success',
                        }),content_type="application/json")
        return HttpResponse(json.dumps({
                    'status':'sth empty',
                    }),content_type="application/json")
    return HttpResponse(json.dumps({
                'status':'wrong method',
                }),content_type="application/json")

    


def admin_user_del(request,user_id):
    acc_model.User.objects(id=user_id).delete()
    return HttpResponseRedirect(reverse('admin:user'))




def admin_site(request):
    bread = u'网站'
    info_list = web_model.Site.objects().all()
    info_head = [u'网站名',u'网站链接',u'创建时间',u'操作']
    return render_to_response(
        u'admin_site.html',
        {
        u'bread':bread,
        u'info_head':info_head,
        u'info_list':info_list,
        })

def admin_domain(request):
    bread = u'主机'
    info_list = web_model.Domain.objects().all()
    info_head = [u'主机名',u'地址连接',u'创建时间',u'所属网站',u'操作']
    return render_to_response(
        u'admin_domain.html',
        {
        u'bread':bread,
        u'info_head':info_head,
        u'info_list':info_list,
        })

def admin_category(request):
    bread = u'类别'
    info_list = web_model.Category.objects().all()
    info_head = [u'种类名',u'地址连接',u'创建时间',u'所属主机',u'操作']
    return render_to_response(
        u'admin_category.html',
        {
        u'bread':bread,
        u'info_head':info_head,
        u'info_list':info_list,
        })

def admin_article(request):
    page  = int(request.GET.get('page',1))
    limit = int(request.GET.get('limit',20))
    bread = u'文章'
    info_count = web_model.Article.objects().count()
    pa = paginate(count=info_count,page=page,limit=limit)
    info_list = web_model.Article.objects[pa['offset']:pa['next_offset']]
    info_head = [u'文章名',u'地址连接',u'创建时间',u'抓取时间',u'作者',u'所属种类',u'操作']
    return render_to_response(
        u'admin_article.html',
        {
        u'bread':bread,
        u'info_head':info_head,
        u'info_list':info_list,
        u'pa':pa,
        })

def admin_author(request):
    page = int(request.GET.get('page',1))
    limit = int(request.GET.get('limit',20))
    bread = u'作者'
    info_count = web_model.Author.objects().count()
    pa = paginate(count=info_count,page=page,limit=limit)
    info_list = web_model.Author.objects[pa['offset']:pa['next_offset']]
    info_head = [u'作者名',u'创建时间',u'操作']
    return render_to_response(
        u'admin_author.html',
        {
        u'bread':bread,
        u'info_head':info_head,
        u'info_list':info_list,
        u'pa':pa,
        })

