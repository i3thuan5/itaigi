import os
from .settings import * # noqa

DEPLOY_HOST = os.getenv('DEPLOY_HOST').split(',')
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SAMESITE = 'Strict'

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

if os.getenv('SSL_REDIRECT', default=True) and DEPLOY_HOST != ['localhost']:
    # Tsi̍t-pîng要求HTTPS，因為localhost開發時袂按呢做，所以開發時關--起-來。
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SECURE_HSTS_SECONDS = 10
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'itaigi',
        'HOST': 'postgres',
        'PORT': '',
    }
}
