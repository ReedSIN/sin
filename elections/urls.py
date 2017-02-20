from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'elections.views',
    (r'^$', 'index'),
    (r'^vote/$', 'vote'),
    (r'^submit_vote/$', 'submit_vote'),
    (r'^results/$', 'results'),
    # (r'^results/(?P<election_id>\d+)/?$', 'results_detail')
    # (r'^admin/$', 'admin_index')
    # (r'^admin/create/$', 'create_election')
    # (r'^admin/delete/(?P<identifier>\d{1,10})/$','delete_election'),
    # (r'^admin/deleted/$', 'deleted')
)
