from django.conf.urls import patterns, include, url
from . import views

app_name = 'sos_grant'
urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'my_application/?$',
        views.manage_application,
        name='manage_application'),
    url(r'my_application/create/?$',
        views.create_application,
        name='create_application'),
    url(r'my_application/edit/?$',
        views.edit_application,
        name='edit_application'),
    url(r'my_application/delete/?$',
        views.delete_application,
        name='delete_application'),
    #admin urls
    url(r'^admin/?$', views.admin_index, name='admin_index'),
    url(r'^admin/create/?$',
        views.admin_create_grant_date,
        name='admin_create_grant_date'),
    url(r'^admin/edit/?$',
        views.admin_edit_grant_date,
        name='admin_edit_grant_date'),
    url(r'^admin/sos_apps/?$',
        views.admin_grant_app_list,
        name='admin_sos_grant_app_list'),
    url(r'^admin/sos_apps/app-(?P<grant_app_id>\d+)/?$',
        views.admin_grant_app_detail,
        name='admin_sos_grant_app_detail'),
    #also add a url for archived seasons
)
