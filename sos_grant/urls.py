from django.conf.urls import patterns, include, url
from . import views 

app_name = 'sos_grant'
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'my_application/?$', views.manage_application, name = 'manage_application'),
    url(r'my_application/view/?$', views.view_application, name = 'view_application'),
    url(r'my_application/create/?$', views.create_application, name = 'create_application'),
    url(r'my_application/edit/?$', views.edit_application, name = 'edit_application'),
    url(r'my_application/delete/?$', views.delete_application, name = 'delete_application'),
    #admin urls
    url(r'^admin/?$', views.admin_index, name='admin_index'),
)
