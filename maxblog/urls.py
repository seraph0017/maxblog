from django.conf.urls import patterns, include, url
from api.user import UserResource
from tastypie.api import Api
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(UserResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maxblog.views.home', name='home'),
    # url(r'^maxblog/', include('maxblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^api/',include(v1_api.urls)),
)
