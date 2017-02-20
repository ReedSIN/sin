from django.conf.urls import url

from appointments import views


urlpatterns = [
  url(r'^$', views.index),
  url(r'^open_positions/(?P<position_id>\d+)/?$', views.open_position_detail),
  url(r'^my_applications/create/(?P<position_id>\d+)/?$', views.create_application),
  url(r'^my_applications/edit/(?P<application_id>\d*)/?$', views.edit_application),
  url(r'^my_applications/delete/(?P<application_id>\d+)/?$', views.delete_application),
  url(r'^admin/?$', views.admin_index),
  url(r'^admin/create/?$', views.create_position),
  url(r'^admin/create/(P<position_id>\d*)/?$', views.submit_new_position),
  url(r'^admin/edit/(?P<position_id>\d*)/?$', views.edit_position),
  url(r'^admin/delete/(?P<position_id>\d+)/?$', views.delete_position),
  url(r'^admin/position-(?P<position_id>\d+)/?$', views.position_application_list),
  url(r'^admin/position-(?P<position_id>\d+)/app-(?P<application_id>\d+)/?$', views.position_application_detail),
  url(r'^admin/submit/(?P<position_id>\d*)/?$', views.submit_new_position),
  url(r'^admin/edit/(?P<position_id>\d*)/?$', views.edit_position),
]
