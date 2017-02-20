from django.conf.urls import url

from identitypoll import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^orgs$', views.create_org),
    url(r'^orgs/(?P<org_id>\d*)/$', views.read_or_update_org),
    url(r'^orgs/(?P<org_id>\d*)/status$', views.org_status),
    url(r'^orgs/(?P<org_id>\d*)/delete$', views.delete_org),
    url(r'^budgets/(?P<org_id>\d*)/$', views.read_or_update_budget),
    url(r'^admin/orgs$', views.admin_index_orgs),
    url(r'^admin/orgs/(?P<org_id>\d*)/$', views.admin_read_or_update_org)
]
