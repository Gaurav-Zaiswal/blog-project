# this file contains only those settings which are used in PRODUCTION
# and extends base.py settings, which has all the default settings

from blog.settings.base import *
from blog.settings.third_party import *


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = os.environ.get('SET_DEBUG')

# replace ip-address and www.website-name.com with respective values
# also put same website name in database['host'], see below database settings
ALLOWED_HOSTS = ['ip-address', 'www.website-name.com']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('SET_DB_NAME'),
        'USER': os.environ.get('SET_DB_USER'),
        'PASSWORD': os.environ.get('SET_DB_PASSWORD'),
        'HOST': os.environ.get('SET_ALLOWD_DB_HOST'),
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
