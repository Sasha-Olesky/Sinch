"""
Django settings for reach project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9xf(cg6(ne-%$_@-iwh@le$9ufbqwlwr#+pn1r3_*u_wxl6)e0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'users',
    'posts',
    'circles',
    'dashboard',
    # rest API
    'rest_framework',
    'rest_framework.authtoken',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'reach.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
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

WSGI_APPLICATION = 'reach.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ufeed.ru@gmail.com'
EMAIL_HOST_PASSWORD = 'lakiboy1316191'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "dev_static"),
)


# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'Reachappreports@gmail.com'
EMAIL_HOST_PASSWORD = 'Reachapp123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# APNS cerf
APNS_CERF_PATH = '/home/ubuntu/reach/project/iphone_ck_prod.pem'
APNS_CERF_SANDBOX_MODE = False

# Lazy load
PAGE_OFFSET = 5
FEED_PAGE_OFFSET = 10

# Group list
GROUPS = [
    "Abuse",
    "Acts of Kindness",
    "Addiction",
    "Anger",
    "Book Suggestions",
    "Bullying",
    "College",
    "Confused",
    "Depression",
    "Disabilities",
    "Divorce",
    "Domestic Violence",
    "Drugs",
    "Eating Disorder",
    "Embarrassment",
    "Fear of...",
    "Feel Good Stories",
    "Financial Issues",
    "First Love",
    "Fitness",
    "Gender issues",
    "Gratitude",
    "Happiness",
    "Health",
    "I Remember When...",
    "Immigration",
    "Insecurities",
    "Issues At Home",
    "Jealousy",
    "LGBTQ",
    "Life is Good...",
    "Marriage Issues",
    "Mental Health",
    "Motivation",
    "Other",
    "Poetry/Lyrics",
    "Positive Vibes",
    "Pressure",
    "Quotes",
    "Relationships",
    "Religion",
    "Resentment",
    "Sadness",
    "School",
    "Self Harm",
    "Sex",
    "Sexuality",
    "Sibling Issues",
    "Sometimes I think About...",
    "Sports",
    "Success",
    "Suicide",
    "Transgender",
    "Venting",
    "Violence",
    "What Happened Today",
    "Who is your Hero?",
    "Work Life"
]
