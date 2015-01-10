from django.conf.urls import patterns, url

from generic.models import *
from generic.views import *

from home import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
)
