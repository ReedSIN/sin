"""
WSGI config for webapps2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site

if os.path.exists("/var/django/webapps2/"):
    site.addsitedir(
        '/var/django/webapps2/env/local/lib/python2.7/site-packages')

    sys.path.append('/var/django/webapps2/')
    sys.path.append('/var/django/webapps2/webapps2/')
    os.environ["DJANGO_SETTINGS_MODULE"] = "webapps2.settings"

    #Activate your virtual env
    activate_env = os.path.expanduser(
        "/var/django/webapps2/env/bin/activate_this.py")
    execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
