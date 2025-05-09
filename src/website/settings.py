"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import environ

from generics.models import Project

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('django_secret_key', default='django-insecure-c0d=s1x9z*e)lo&^)26i_+ina3&le2c_$$2p7hgsp*ytn8orqh')

GCP_CLIENT_ID = env('gcp_client_id', default='None')
GCP_SECRET = env('gcp_secret', default='None')
STRIPE_PUBLIC_KEY = env('stripe_public_key', default=None)
STRIPE_SECRET_KEY = env('stripe_secret_key', default=None)
STRIPE_WEBHOOK_SECRET = env('stripe_webhook_secret', default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default='True').lower() in ('true', '1', 't')  # Todo: Ne laisse pas à "True" en prod !!!!!
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['http://127.0.0.1'])

# Application definition

MULTI_SITE_PATTERNS = {
    # Dev en local => DOMAIN_NAME: APP_NAME (tu peux tester 2 projets différents en simultané en local)
    'localhost': Project(app_name='project_1', display_name='Project 1'),
    '127.0.0.1': Project(app_name='project_2', display_name='Project 2'),
    'http://i400gkkkw888o008ccksc0gk.144.126.216.185.sslip.io/': Project(app_name='my_first_saas', display_name='my_first_saas'),

    # Production
    # EXAMPLE => 'rapidsaas.fr': Project(app_name='rapidsaas', display_name='Rapid SaaS')
}

for domain in MULTI_SITE_PATTERNS.keys():
    ALLOWED_HOSTS.append(domain)
    if domain in ['localhost', '127.0.0.1']:
        continue
    CSRF_TRUSTED_ORIGINS.append(f"https://{domain}")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Project apps
    'payments',
    'generics',
    'authentications',

    # Third party apps
    'compressor',
    'simple_history',
    'django_htmx',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
] + list(set([project.app_name for _, project in MULTI_SITE_PATTERNS.items()]))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'generics.middlewares.DynamicDomainRedirectMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_NAME', default='postgres'),
            'USER': os.environ.get('POSTGRES_USER', default='postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default='postgres'),
            'HOST': os.environ.get('POSTGRES_HOST', default='db'),
            'PORT': int(os.environ.get('POSTGRES_PORT', default=5432)),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
AUTH_USER_MODEL = 'authentications.CustomUser'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = DEBUG

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# SITE_ID = 3
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_LOGIN_ON_GET = True
# SOCIALACCOUNT_ADAPTER = 'authentications.models.UserAccountAdapter'
LOGIN_REQUIRED_URL = '/accounts/google/login/?process=login'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': GCP_CLIENT_ID,
            'secret': GCP_SECRET,
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
