from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'sos_grant.views',
    (r'^$','index'),
    (r'my_application/?$', 'manage_application'),
    (r'my_application/view/?$', 'view_application'),
    (r'my_application/create/?$', 'create_application'),
    (r'my_application/edit/?$', 'edit_application'),
    (r'my_application/save/?$', 'save_application'),
    (r'my_application/submit/?$', 'submit_application'),
    (r'my_application/delete/?$', 'delete_application'),
    # (r'my_application/save/?$', 'save_application'), or just go back to apply/submit
)
