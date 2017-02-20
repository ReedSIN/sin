from django.conf.urls import url

from elections import views

urlpatterns = [
    url(r'^$',  views.index),
    url(r'^vote/$',  views.vote),
    url(r'^submit_vote/$',  views.submit_vote),
    url(r'^results/$',  views.results),
    # (r'^results/(?P<election_id>\d+)/?$', 'results_detail')
    # (r'^admin/$', 'admin_index')
    # (r'^admin/create/$', 'create_election')
    # (r'^admin/delete/(?P<identifier>\d{1,10})/$','delete_election'),
    # (r'^admin/deleted/$', 'deleted')
]
