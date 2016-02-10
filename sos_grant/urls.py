from django.conf.urls import patterns, include, url
from . import views 

app_name = 'sos_grant'
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'my_application/?$', views.manage_application, name = 'manage_application'),
    url(r'my_application/create/?$', views.create_application, name = 'create_application'),
    url(r'my_application/edit/?$', views.edit_application, name = 'edit_application'),
    url(r'my_application/delete/?$', views.delete_application, name = 'delete_application'),
    #admin urls
    url(r'^admin/?$', views.admin_index, name='admin_index'),
    url(r'^admin/create/?$', views.admin_create_grant_season, name='admin_create_position'),
    url(r'^admin/edit/(?P<position_id>\d*)/?$','edit_position'),
    url(r'^admin/delete/(?P<position_id>\d+)/?$','delete_position'),
    url(r'^admin/position-(?P<position_id>\d+)/?$','position_application_list'),
    url(r'^admin/position-(?P<position_id>\d+)/app-(?P<application_id>\d+)/?$','position_application_detail'),
    url(r'^admin/submit/(?P<position_id>\d*)/?$','submit_new_position'),
    url(r'^admin/edit/(?P<position_id>\d*)/?$','edit_position'),
    #also add a url for archived seasons
)
