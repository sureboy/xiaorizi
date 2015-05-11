# Django settings for LifeExpert project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
DATABASES = {
    #'default': {
    #    'ENGINE':'django.db.backends.mysql',
    #    'NAME': 'vevent',
    #    'USER': 'writeuser',
    #    'PASSWORD': 'ghk*LoY5,;:/?',
    #    'HOST': '10.10.59.222',
    #    'PORT': '3306',
    #},
    #'slave': {
    #    'ENGINE':'django.db.backends.mysql',
    #    'NAME': 'vevent',
    #    'USER': 'readuser',
    #    'PASSWORD': 'ghk*LoY5,;:/?',
    #    'HOST': '10.10.64.15',
    #    'PORT': '3306',
    #}, 
    #'user_center_w': {
    #    'ENGINE':'django.db.backends.mysql',
    #    'NAME': 'user_center',
    #    'USER': 'usercenter',
    #    'PASSWORD': 'ghk*LoY5,;:/k?',
    #    'HOST': '10.10.59.222',
    #    'PORT': '3306',
    #} ,
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME': 'user_center',
        'USER': 'usercenter',
        'PASSWORD': 'ghk*LoY5,;:/k?',
        'HOST': '10.10.59.222',
        'PORT': '3306',
    }
}

#DATABASE_ROUTERS = ['LifeExpert.DBRouter.Router']
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False


#MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../media").replace('\\', '/')
MEDIA_ROOT = '/data/web/LifeExpert/media'
MEDIA_URL = "/site_media/"

#STATIC_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../static").replace('\\', '/')
STATIC_ROOT = '/data/web/LifeExpert/static'
STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'
#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '13*54g++9+xnfamrp2-l*-mi(pf&w3f8b6f(!%qi31c*@qqefv'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'urls_admin'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'LifeExpert.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'LifeApi',
    'User',
    'Ticket',
    'sponsor',
    'weibo_data',
    #'NewAppApi',
    #'user_activity',
    #'spot',
    #'app_manage',
    # Uncomment the next line to enable the admin:
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': { 
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data/tmp/','life_all.log'),  
            'maxBytes': 1024*1024*5,  
            'backupCount': 5,
            'formatter':'standard',
        },
        
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data/tmp/','script.log'),  
            'maxBytes': 1024*1024*5,  
            'backupCount': 5,
            'formatter':'standard',
        },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/data/tmp/','script.log'),   
            'maxBytes': 1024*1024*5, 
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {

        'XieYin.app':{
            'handlers': ['default','console'],
            'level': 'DEBUG',
            'propagate': True        
        },

    }
}  
CACHES ={
         'default':{
            'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION':'10.10.59.222:11211',
            'OPTIONS':{
                'MAX_ENTRIES':100000,
                'CULL_FREQUENCY':10
            }
        }
}