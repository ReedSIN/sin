from django.conf.urls import url

from organizations import views


VALID_FACTORS = [
    'student',
]


urlpatterns = [
    url(r'^$', views.index),
    url(r'^new/$', views.new_org),
    url(r'^edit/(?P<org_id>\d*)/?$', views.edit_org),
    url(r'^save/(?P<org_id>\d*)/?$', views.save_org),
    url(r'^add_signators/?$', views.add_signators),
    url(r'^delete/(?P<org_id>\d+)/?$', views.delete_org),
    url(r'^(?P<org_id>\d+)/?$', views.organization_detail),
    url(r'^organization_list.csv?$',views.csv_list),
    url(r'^orgs/(?P<org_id>\d+)/change-signator/?$', views.change_signator_get),
    url(r'^orgs/(?P<org_id>\d+)/change-signator/submit/?$', views.change_signator_post),
    url(r'^manage-signators/?$', views.manage_signators),
    url(r'^remove_signator/(?P<sig_id>\d+)/??$', views.remove_signator)
]
