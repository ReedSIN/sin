"""
Django settings for webapps2 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMINS = (
    ('Will Jones', 'wjones@reed.edu'),
    ('Alex Pan', 'pana@reed.edu'),
    ('Chris Henn', 'hennc@reed.edu'),
#    ('Isabella Jorissen','isjoriss@reed.edu'),
    )

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
SERVER_EMAIL = 'noreply@sin.reed.edu'
EMAIL_USE_TLS = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/


ALLOWED_HOSTS = [
    '.reed.edu',
    'localhost'
]


CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'generic',
    'organizations',
    'finance',
    'fundingpoll',
    'elections',
    'appointments',
    'sos_grant',
    'activelink',
    'identitypoll'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bugsnag.django.middleware.BugsnagMiddleware',
)

ROOT_URLCONF = 'webapps2.urls'

WSGI_APPLICATION = 'webapps2.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = 'staticfiles/'
STATICFILES_DIRS = (
    'webapps_assets/',
    'bower_components/',
)

# Email for the server
EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'noreply@sin.reed.edu'


# TEMPLATE_DIRS = (
#     '/webapps2/templates/',
# )
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request"
)

from local_settings import *
