import os,sys
from utils import jammit
from mongoengine import connect
from pymongo import Connection

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH		= os.path.dirname(os.path.abspath(__file__))
CURRENT_DIR			= os.path.dirname(__file__)
TEMPLATE_DIRS		= (os.path.join(CURRENT_DIR, '../','templates'),)
STATICFILES_DIRS	= (os.path.join(CURRENT_DIR, '../','static'),)
MEDIA_ROOT			= os.path.join(CURRENT_DIR, '../','media')
MEDIA_URL			= '/media/'
JAMMIT				= jammit.JammitAssets(os.path.join(PROJECT_PATH,  '../' ))


ADMINS = (
    ('Joseph Misiti', 'joseph.misiti@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

MANAGERS = ADMINS
MONGODB = {
			'db': 'telegraphandmain',
			'options': {
				'host': '127.0.0.1',
				'port': 27017
				}
			}

connect(MONGODB['db'], host=MONGODB['options']['host'],port=MONGODB['options']['port'] )


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL						= '/media/'
STATIC_ROOT						= ''
STATIC_URL						= '/static/'
ADMIN_MEDIA_PREFIX				= '/static/admin/'
POSTS_PER_PAGE					= 10

# amazon 
AWS_ACCESS_KEY = 'AKIAIHEXGZKFEZPKGKTQ'
AWS_SECRET_KEY = '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'
AWS_BUCKET_NAME = 'elementcycle'

LOGIN_REDIRECT_URL		= '/home/'
LOGIN_URL				= '/login/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd2^br_66d&amp;nzd8*4_!@=a)m1%ynfc9ljqltvc!!_r3swrwh4k%'

# List of callables that know how to import templates from various sources.
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

ROOT_URLCONF = 'telegraphandmain.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'telegraphandmain.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.sessions',
	'apps.static',

)

AUTHENTICATION_BACKENDS = ('mongoengine.django.auth.MongoEngineBackend',)
SESSION_ENGINE 			= 'mongoengine.django.sessions'

try:
	from local_settings import *
except ImportError, e:
	pass
	

if not DEBUG:
	DJANGO_LOG_PATH = '/var/log/telegraphandmain.log'
	INSTALLED_APPS += (
		'gunicorn',
	)
else:
	DJANGO_LOG_PATH = os.path.join(PROJECT_PATH,'misc', 'telegraphandmain.log')
	
ALLOWED_HOSTS = [ 'www.telegraphandmain.com', '*.telegraphandmain.com','localhost', '127.0.0.1']

try:
	from config.gunicorn_conf import *
except ImportError, e:
	pass


try:
	from local_settings import *
except ImportError, e:
	pass	

	
	
LOGGING = {
	    'version': 1,
	    'disable_existing_loggers': False,
	    'formatters': 
		{
	        'verbose': 
			{
	            'format': '[%(asctime)s][%(levelname)s] | %(message)s', 
	            'datefmt': '%b %d %H:%M:%S'
	        },
	        'simple': 
			{
	            'format': '[%(asctime)s][%(levelname)s] %(name)s | %(message)s'
	        },
	    },
		'filters': {
		     'require_debug_false': {
		         '()': 'django.utils.log.RequireDebugFalse'
		     }
		 },
	    'handlers': 
		{
	        'null': {
	            'level':'DEBUG',
	            'class':'django.utils.log.NullHandler',
	        },
	        'console':{
	            'level': 'DEBUG',
	            'class': 'logging.StreamHandler',
	            'formatter': 'verbose'
	        },
	        'log_file':{
	            'level': 'DEBUG',
	            'class': 'logging.handlers.RotatingFileHandler',
	            'filename': DJANGO_LOG_PATH,
	            'maxBytes': '16777216', # 16megabytes
	            'formatter': 'verbose'
	        },
	        'mail_admins': {
	            'level': 'ERROR',
				'filters': ['require_debug_false'],
	            'class': 'django.utils.log.AdminEmailHandler',
	            'include_html': True,
	        }
		},
	    'console':
		{
	            'level': 'DEBUG',
	            'class': 'logging.StreamHandler',
	            'formatter': 'verbose'
	    },
	    'log_file':{
	        'level': 'DEBUG',
	        'class': 'logging.handlers.RotatingFileHandler',
	        'filename': DJANGO_LOG_PATH,
	        'maxBytes': '16777216', # 16megabytes
	        'formatter': 'verbose'
	    },
	    'loggers': {
	        'django.request': {
	            'handlers': ['mail_admins'],
	            'level': 'ERROR',
	            'propagate': True,
	        },
	        'django.db.backends': {
	            'handlers': ['null'],
	            'level': 'DEBUG',
	            'propagate': False,
	        },
	        'socialq': {
	            'handlers': ['console', 'log_file'],
	            'level': 'DEBUG',
	            'propagate': False,
	        },
	    'apps': {
	            'handlers': ['log_file'],
	            'level': 'INFO',
	            'propagate': True,
	        },
		}
	}

