from django.conf.urls import patterns, include, url
from api.user import UserResource
import api.webanapi
from api.webanapi import SiteResource,ArticleResource,AuthorResource,DomainResource,CategoryResource
from tastypie.api import Api
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(SiteResource())
v1_api.register(ArticleResource())
v1_api.register(DomainResource())
v1_api.register(CategoryResource())
v1_api.register(AuthorResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maxblog.views.home', name='home'),
    # url(r'^maxblog/', include('maxblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^webanan/', include('webanan.urls',namespace='webanan')),
    url(r'^admin/', include('admin.urls',namespace='admin')),
    url(r'^api/',include(v1_api.urls)),
)
