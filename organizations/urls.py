from django.conf.urls import patterns, include, url

VALID_FACTORS = [
    'student',
    ]


urlpatterns = patterns(
    'organizations.views',
    url(r'^$', 'index'),
    url(r'^new/$', 'new_org'),
    url(r'^edit/(?P<org_id>\d*)/?$', 'edit_org'),
    url(r'^save/(?P<org_id>\d*)/?$', 'save_org'),
    url(r'^add_signators/?$', 'add_signators'),
    url(r'^delete/(?P<org_id>\d+)/?$', 'delete_org'),
    url(r'^(?P<org_id>\d+)/?$', 'organization_detail'),
    url(r'^organization_list.csv?$','csv_list'),
    url(r'^orgs/(?P<org_id>\d+)/change-signator/?$', 'change_signator_get'),
    url(r'^orgs/(?P<org_id>\d+)/change-signator/submit/?$', 'change_signator_post'),
    url(r'^manage-signators/?$', 'manage_signators'),
    url(r'^remove_signator/(?P<sig_id>\d+)/??$', 'remove_signator'),    
)
