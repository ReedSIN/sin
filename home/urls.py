from django.conf.urls import patterns, url

from generic.models import *
from generic.views import *

from home import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^home/?', views.index, name='index'),
                       url(r'^check_user/?', check_user),
                       url(r'^search_orgs/?', search_orgs)
)
