"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from importlib import import_module
import os
import sys

# django
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# local settings
if 'CIRCLECI' in os.environ:
    local_settings = import_module('project.circleci_settings')
else:
    local_settings = import_module('project.local_settings')

DEBUG = local_settings.DEBUG
LOCAL_DATABASES = local_settings.LOCAL_DATABASES
LOCALLY_INSTALLED_APPS = local_settings.LOCALLY_INSTALLED_APPS
ENABLE_EMAILS = local_settings.ENABLE_EMAILS
ADMINS = local_settings.ADMINS
LOCALLY_ALLOWED_HOSTS = local_settings.LOCALLY_ALLOWED_HOSTS
SECRET_KEY = local_settings.SECRET_KEY


def get_local_value(key, default_value):
    try:
        return getattr(local_settings, key)
    except AttributeError:
        return default_value


GOOGLE_ANALYTICS_CODE = get_local_value('GOOGLE_ANALYTICS_CODE', None)

# default keys, replace with somethign your own
RECAPTCHA_PUBLIC_KEY = get_local_value('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = get_local_value('RECAPTCHA_PRIVATE_KEY', '')
# To use the new No Captcha reCaptcha
NOCAPTCHA = True


if DEBUG:
    env = 'development'
else:
    env = 'production'

# TEST should be true if we are running python tests
TEST = 'test' in sys.argv


# People who get code error notifications.
# In the format [
#     ('Full Name', 'email@example.com'),
#     ('Full Name', 'anotheremail@example.com'),
# ]
ADMINS = ADMINS

# List of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = [
    '127.0.0.1',
]


PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

ALLOWED_HOSTS = []
ALLOWED_HOSTS += LOCALLY_ALLOWED_HOSTS

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # required apps
    'base.apps.BaseConfig',
    'users',

    # external
    'captcha',
    'loginas',
    'rest_framework',
    'webpack_loader',

    # internal
    'regions',
    'parameters',
]

# Email settings, uncomment if your project sends emails
# You must set this values in local_settings
# EMAIL_HOST = get_local_value('EMAIL_HOST', '')
# EMAIL_HOST_USER = get_local_value('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = get_local_value('EMAIL_HOST_PASSWORD', '')
# EMAIL_PORT = get_local_value('EMAIL_PORT', 587)
# EMAIL_EMAIL_USE_TLS = get_local_value('EMAIL_USE_TLS', True)

# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
EMAIL_SENDER_NAME = 'My project'

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    # Set the apps that are installed locally
    # only if we are on debug should we have locally installed apps
    INSTALLED_APPS = INSTALLED_APPS + LOCALLY_INSTALLED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.RequestMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
    ]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.context_processors.google_analytics_code',
            ],
            'loaders': [
                ('pypugjs.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ],
            'builtins': ['pypugjs.ext.django.templatetags'],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {}
DATABASES.update(LOCAL_DATABASES)

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
if DEBUG or not ENABLE_EMAILS:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Santiago'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LOCALE_PATHS = [
    PROJECT_DIR + '/locale'
]

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')
MEDIA_URL = '/uploads/'

if not DEBUG:
    STATICFILES_DIRS = [
        # Webpack bundles
        ('bundles', os.path.join(BASE_DIR, 'assets/bundles')),
    ]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

##################
# AUTHENTICATION #
##################

AUTH_USER_MODEL = 'users.User'
LOGOUT_REDIRECT_URL = '/'

# set the precompilers
COMPRESS_PRECOMPILERS = (
    ('text/pug', 'base.filters.pug.PugCompilerFilter'),
)

# un comment when we start using only SSL
# RECAPTCHA_USE_SSL = True
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': (
                '%(asctime)s %(levelname)s: file %(filename)s line %(lineno)d '
                '%(message)s'
            )
        },
    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'standard',
            'level': 'ERROR',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '{}/logs/{}/error.log'.format(BASE_DIR, env),
            'formatter': 'standard',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# ### Login as settings ###
CAN_LOGIN_AS = "base.utils.can_loginas"
LOGOUT_URL = reverse_lazy('loginas-logout')
LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy('admin:index')

# CACHE
if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": False,
        "BUNDLE_DIR_NAME": "bundles/",
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": 1,  # 1 second timeout for webpack compilation
        "IGNORE": [r'.+\.hot-update.js', r'.+\.map']
    }
}

FILE_UPLOAD_PERMISSIONS = 0o644


# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
}


if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

# The change's information of this fields will be ignored in the logs
LOG_SENSITIVE_FIELDS = [
    'password',
]

# These fields will be ignored in the logs
LOG_IGNORE_FIELDS = [
    'created_at',
    'updated_at',
    'original_dict',
    'id',
    'date_joined',
]

# django-cron
CRON_CLASSES = [
    'base.cron.ClearSessionsCronJoab',
]
