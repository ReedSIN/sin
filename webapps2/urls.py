from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'webapps2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('home.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^appointments/', include('appointments.urls')),
    url(r'^organization-manager/', include('organizations.urls')),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^finance/', include('finance.urls')),
    url(r'^fundingpoll/', include('fundingpoll.urls')),
    url(r'^elections/', include('elections.urls')),
)
