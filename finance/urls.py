from django.conf.urls import url

from finance import views

urlpatterns = [
    url(r'^view_budgets/(?P<budget_id>\d+)/?$',  views.view_one_budget),
    url(r'^view_budgets/?$',  views.view_all_budgets),
    url(r'^view_budgets/respond/edit/(?P<budget_id>\d+)/?$',  views.budget_respond_get),
    url(r'^view_budgets/respond/save/(?P<budget_id>\d+)/?$',  views.budget_respond_post, name = 'finance-budget-respond-post'),
    url(r'^approved_budgets/?$',  views.view_approved_budgets),
    url(r'^submit_budget/?$',  views.create_budget),
    url(r'^submit_budget/create/?(?P<budget_id>\d*)/?$',  views.edit_my_budget_post),
    url(r'^my_budgets/?$',  views.my_budgets),
    url(r'^my_budgets/edit/(?P<budget_id>\d+)/?$',  views.edit_my_budget),
    url(r'^my_budgets/save/(?P<budget_id>\d+)/?$',  views.edit_my_budget_post),
    url(r'^my_budgets/delete/(?P<budget_id>\d+)/?$',  views.delete_my_budget),
    url(r'^organization_budgets?$',  views.budget_search),
    url(r'^$',  views.index),
    url(r'^signator',  views.add_signator),
    url(r'^api/approved_budgets/?',  views.json_approved_budgets),
    url(r'^api/unapproved_budgets/?',  views.json_unapproved_budgets)
]
