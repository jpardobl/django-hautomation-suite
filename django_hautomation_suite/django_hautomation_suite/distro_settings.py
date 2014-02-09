# Django settings for django_hautomation_suite project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#used by the haweb to find the REST API server
HA_SERVER = "HA_REST_API_HOST"
HA_PASSWORD = "HA_REST_API_PASSWORD"
HA_USERNAME = "HA_REST_API_USERNAME"


DJANGO_HAUTOMATION_DEPLOYED = HA_DJANGO_HAUTOMATION_DEPLOYED
DJANGO_HAWEB_DEPLOYED = HA_DJANGO_HAWEB_DEPLOYED
DJANGO_THERMOMETER_DEPLOYED = HA_DJANGO_THERMOMETER_DEPLOYED
DJANGO_THERMOSTAT_DEPLOYED = HA_DJANGO_THERMOSTAT_DEPLOYED

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.HA_DB_TYPE', 
        'NAME': 'HA_DB_NAME', 
        'USER': 'HA_DB_USER',
        'PASSWORD': 'HA_DB_PASSWORD',
        'HOST': 'HA_DB_HOST',
        'PORT': 'HA_DB_PORT', 
    }
}

ALLOWED_HOSTS = ["HA_WEB_SERVER_NAME", ]

TIME_ZONE = 'HA_TIME_ZONE'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = 'HA_STATIC'

STATIC_URL = '/static/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'cr!vx#to^+*^y8*_0)_c25*4p(ksxb1=uwo*-zch+um(7d)631'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_hautomation_suite.urls'

WSGI_APPLICATION = 'django_hautomation_suite.wsgi.application'

TEMPLATE_DIRS = ()

INSTALLED_APPS = (
    #defaul apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #project apps
    "ha_cfg",
    "hacore",
    "harest",
    "haweb",
    "compressor",
    "django_thermometer",
    "django_thermostat",
    'django.contrib.admin',
    'gunicorn',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
