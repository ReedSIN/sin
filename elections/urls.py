from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'elections.views',
    (r'^$', 'index'),
    (r'^vote/?$', 'vote')
)
