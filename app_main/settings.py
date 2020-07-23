import os
import django_heroku
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_fsm_log",
    "subscriptions.apps.SubscriptionsConfig",
    'multiselectfield',
    "app_db_logger"
    "app_web",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app_main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "app_main.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }

# Logger
# https://docs.djangoproject.com/en/3.0/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{name} {bot_username} {levelname} {asctime} {module} {process:d} {processName} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{name} {bot_username} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'app_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"

django_heroku.settings(locals())
""" 
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERYBEAT_SCHEDULE = {
    "subscriptions_renewals": {
        "task": "subscriptions.tasks.trigger_renewals",
        "schedule": crontab(hour=0, minute=10),
    },
    "subscriptions_expiring": {
        "task": "subscriptions.tasks.trigger_expiring",
        "schedule": crontab(hour=0, minute=15),
    },
    "subscriptions_suspended": {
        "task": "subscriptions.tasks.trigger_suspended",
        "schedule": crontab(hour="3,6,9", minute=30),
    },
    "subscriptions_suspended_timeout": {
        "task": "subscriptions.tasks.trigger_suspended_timeout",
        "schedule": crontab(hour=0, minute=40),
        "kwargs": {"hours": 48},
    },
    "subscriptions_stuck": {
        "task": "subscriptions.tasks.trigger_stuck",
        "schedule": crontab(hour="*/2", minute=50),
        "kwargs": {"hours": 2},
    },
}
 """