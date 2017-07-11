"""
Django settings for media project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
#import ldap
import django_auth_ldap.config
#import LDAPSearch, GroupOfNamesType
from .databasesettings import DATABASES
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*1d5m!lnpp(yp4a13vr%b9vanjf)euhr7_a*o)$en&esim0jm-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

COMPRESS_OFFLINE=True
COMPRESS_ENABLED=True



# Application definition

INSTALLED_APPS = [
    'store.apps.StoreConfig' ,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'django_extensions',
    'jquery',
    'djangoformsetjs',
#    'hijack',
#    'south',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'media.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'media.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


HIJACK_LOGIN_REDIRECT_URL = "/"
REVERSE_HIJACK_LOGIN_REDIRECT_URL = "/admin/"
HIJACK_NOTIFY_ADMIN = True

#Setting up LDAP Authentication:

AUTHENTICATION_BACKENDS = (
    #'TimeMatrix.backend.LDAPBackend',
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_LDAP_SERVER_URI = "ldap://ldap-vip1.int.janelia.org"
'''
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,dc=hhmi,dc=org",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
)

"""class CustomGroupOfNamesType(GroupOfNamesType):
    """"""
    An LDAPGroupType subclass that handles groups of class groupOfNames.

    The purpose of this whole class is to remove the begining string (base_dn)
    from the group name since it is way too long.
    
    def __init__(self, base_dn):
        self.base_dn = base_dn
        super(CustomGroupOfNamesType, self).__init__('dn')
    
    def group_name:
        Given the (DN, attrs) 2-tuple of an LDAP group, this returns the name of
        the Django group. This may return None to indicate that a particular
        LDAP group has no corresponding Django group.
        
        The base implementation returns the value of the cn attribute, or
        whichever attribute was given to __init__ in the name_attr
        parameter.
        """"""
        try:
            name = group_info[0].replace(self.base_dn,'')
        except (KeyError, IndexError):
            name = None
        
        return name

# More secure
#AUTH_LDAP_START_TLS = True

# Set up the basic group parameters.  We're only searching the ApplicationRoles
# group, I think
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=ApplicationRoles,dc=hhmi,dc=org",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)")
AUTH_LDAP_GROUP_TYPE = CustomGroupOfNamesType("ou=ApplicationRoles,dc=hhmi,dc=org")

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

#An option for later if we have specific groups
#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
#    "can_view_summary_all_fly_olympiad":"cn=view_summary,ou=all,ou=FlyOlympiad,ou=ApplicationRoles,dc=hhmi,dc=org",
#    "can_view_summary_aggression_fly_olympiad":"cn=view_summary,ou=aggression,ou=FlyOlympiad,ou=ApplicationRoles,dc=hhmi,dc=org"
#}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True #Not sure what this does
AUTH_LDAP_MIRROR_GROUPS = False #Pulls in LDAP groups, overwrites custom groups :-(

# Optional Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = False 
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

#customize app log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default':{
            'format':'%(levelname)s %(asctime)s %(module)s: %(message)s'
        }
    },
    'handlers':{
        'default':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'default': {
            'handlers': ['default'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

try:
    from local_settings import *
except ImportError:
    pass"""
'''
