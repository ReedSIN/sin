"""
Example local settings. Copy this into a 'local_settings.py' file, and it will be imported by
settings.py.
"""
BUGSNAG = {
    "api_key": "insert api key here"
}

# Cookie Path - to make sure it isn't confused with other django sessions
# but it screws up cosign. So nevermind for now.
SESSION_COOKIE_PATH="/webapps2"

STATIC_URL = '/static/'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newwebapps',
        # The following settings are not used with sqlite3
        'USER': 'sin',
        'PASSWORD': 'krogerrulz',
        'HOST': 'localhost',
        'PORT': '',
#        'OPTIONS': 'SET foreign_key_checks = 0;',
    }
}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wouldnt you like to know?'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

TEST = True
