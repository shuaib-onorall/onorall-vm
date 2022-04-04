"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from pathlib import Path
import os
from pickle import APPEND



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dl!6%!y5!6jbqe0&ay8g^jox!w%=&mqf*bzquiy&$mj&w(_2lj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.95' , '127.0.0.1'] #['https://cretskill-backend.herokuapp.com/'] #'192.168.1.85'


# Application definition 

INSTALLED_APPS = [
    'myapp' ,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders", #this is used for integerate with the server
    'django.contrib.sites', # this is also used for google signup
    'allauth',  #this is used for  google signup
    'allauth.account',
    'django_filters',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'channels',
    'rest_framework_simplejwt',

    'ws4redis',



    'embed_video' , # for embed videos
    #'debug_toolbar' ,   # for debugging
    #'locust',        # testing api
    
]

SITE_ID=1

#___________________________________________________________________
MIDDLEWARE = [
    


    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    #ye white noise file requirement k hisaab se hai
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'frontend','build')],
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


# for embed videos !pip install django-embed-video
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',)

#WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION= 'backend.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

''''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'myonorall',
        'CLIENT': {
           'host': 'mongodb+srv://amitsingh:onorall@cluster0.ypmmy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
            
        }
    }
}


#configuration redis implementation for the channels .it is used for the notifications
CHANNEL_LAYERS = {
    'default': {
     
       
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
             "hosts": [('127.0.0.1', 6379)],
        },

        ### Method 3: Via In-memory channel layer
        ## Using this method.
      # "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/
TIME_ZONE = 'Asia/Kolkata'  # 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'frontend', 'build', 'static'),
    ]

#this is for media configuration

MEDIA_ROOT= os.path.join(BASE_DIR, 'media/')
MEDIA_URL= "/media/"

ENFORCE_SCHEMA=False #this can will be help  you to stop the migration after this you don,t have to migrate again and again.

# this allow for the inetgeration for the server
CORS_ORIGIN_ALLOW_ALL = True

#this authentication backend is used ofr google signup
AUTHENTICATION_BACKENDS=[
    'django.contrib.auth.backends.ModelBackend', 
    'allauth.account.auth_backends.AuthenticationBackend'
]

#mongo_engine
SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'

SITE_ID=1
LOGIN_REDIRECT_URL='/'

#mongo
SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


#param error

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
     )
 }

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '539031140956-alq5ce9fih1c5n4sl8vtc4tq0f4j1k49.apps.googleusercontent.com',
            'secret': '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',
            
        }
    }
}

#simple jwt
REST_FRAMEWORK = {
   
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    #'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    #'PAGE_SIZE': 1000
    
}

#configure for the simple jwt
from datetime import timedelta


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



#send emails for document verification
SITE_HOST = '192.168.1.85:8000'
DEFAULT_FROM_EMAIL ='amitsofficial1998@gmail.com'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend' #this is used for the backend
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='amitsofficial1998@gmail.com'
EMAIL_HOST_PASSWORD='Amit@1998'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_SSL=False


#for search functionality
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

#api key
API_KEY = 'e3ffa140-7c63-11ec-b9b5-0200cd936042'

#__________________________________________________________________________________________________________________________
#for heroku purposes
# import django_on_heroku
# django_on_heroku.settings(locals())



###  DJANGO DEBUG SETTING FOR DEVELOPMENT
if DEBUG:
    INTERNAL_IPS = ( '*' ) # '127.0.0.1', '192.168.1.95' , 
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False,} 
def show_toolbar(request):
    return True
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK" : show_toolbar,}
import mimetypes
mimetypes.add_type("application/javascript", ".js", True)

#________________ END DEBUG SETTING _________________