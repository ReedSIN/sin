from django.conf.urls import patterns

urlpatterns = patterns(
    'identitypoll.views', (r'^$', 'index'), (r'^orgs$', 'create_org'),
    (r'^orgs/(?P<org_id>\d*)/$', 'read_or_update_org'),
    (r'^orgs/(?P<org_id>\d*)/status$', 'org_status'),
    (r'^orgs/(?P<org_id>\d*)/delete$', 'delete_org'),
    (r'^budgets/(?P<org_id>\d*)/$', 'read_or_update_budget'),
    (r'^admin/orgs$', 'admin_index_orgs'),
    (r'^admin/orgs/(?P<org_id>\d*)/$', 'admin_read_or_update_org'))
