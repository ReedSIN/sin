from django.conf.urls import url

from fundingpoll import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^vote/?$', views.vote_main),
    url(r'^vote/submit/?$', views.submit_vote),
    url(r'^my_registrations/?$',  views.my_registrations),
    url(r'^my_registrations/save/?$', views.save_registration),
    url(r'^registered/?$',  views.registered),
    url(r'^results/?$', views.view_results),
    url(r'^results_json/?$',  views.view_results_json),
    url(r'^schedule/?$', views.schedule),
    url(r'^budgets/edit/(?P<org_id>\d*)/?$',  views.edit_budget),
    url(r'^budgets/save/(?P<budget_id>\d*)/?$',  views.save_budget),
    url(r'^budgets/preview/(?P<budget_id>\d+)/?$',  views.preview_budget),
    url(r'^budgets/csv-list/?$', views.csv_budget_list),
    url(r'^admin/results/?$', views.admin_view_results),
    url(r'^admin/voting/?$',  views.admin_voting),
#  (r'^admin/register/?$', 'admin_registration'),
#  (r'^admin/budgets/edit/(?P<org_id>\d*)/?$', 'admin_edit_budget'),
#  (r'^admin/budgets/save/(?P<org_id>\d*)/?$', 'admin_save_budget'),
    url(r'^admin/view_budgets/?$',  views.view_all_budgets),
    url(r'^admin/view_budgets/(?P<budget_id>\d+)/?$',  views.view_one_budget),
    url(r'^admin/top40emails$',  views.top_40_emails)
]
