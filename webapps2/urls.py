from django.conf.urls import include, url
from django.contrib import admin

import generic

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^appointments/', include('appointments.urls')),
    url(r'^organization-manager/', include('organizations.urls')),
    url(r'^organizations/', include('organizations.urls')),
    url(r'^finance/', include('finance.urls')),
    url(r'^fundingpoll/', include('fundingpoll.urls')),
    url(r'^identitypoll/', include('identitypoll.urls')),
    url(r'^elections/', include('elections.urls')),
    url(r'^sos_grant/', include('sos_grant.urls', namespace="sos_grant")),
    url('logout', generic.views.logout)
]
