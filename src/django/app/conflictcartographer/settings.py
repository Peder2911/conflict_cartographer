"""
Conflict cartographer settings
"""
from environs import Env
import os


env = Env()
env.read_env()

# ================================================
# ================================================
# ================================================
# DYNAMIC CONFIG
# These settings are overridden by env variables,
# and typically vary between dev. and prod. 
# settings.
# ================================================
# ================================================
# ================================================

SECRET_KEY = env.str("SECRET_KEY","0"*128)

ACTIVE     = env.bool("APP_DISABLED", True)
DEBUG      = not env.bool("PRODUCTION", False)


DATABASES = {
        "default":{
            "ENGINE":       "django.db.backends.postgresql_psycopg2",
            "HOST":         env.str("DB_HOST",         "0.0.0.0"),
            "PORT":         env.str("DB_PORT",         "2345"),
            "USER":         env.str("DB_USER",         "fakedata"),
            "PASSWORD":     env.str("DB_PASSWORD",     "fakedata"),
            "NAME":         env.str("DB_NAME",         "fakedata"),
            "CONN_MAX_AGE": env.int("DB_CONN_MAX_AGE", 3600)
        }
}

DB_SSL = env.bool("DB_SSL", False)

if DB_SSL:
    DATABASES["default"].update({
        "OPTIONS":{
            "sslmode":     "require",
            "sslrootcert": env.str("DB_SSL_CERT","/cert/BaltimoreCyberTrustRoot.crt.pem")
            }
        })

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST    = True

# ================================================
# ================================================
# ================================================
# STATIC CONFIG
# These settings do not change between dev. 
# and prod.
# ================================================
# ================================================
# ================================================

ALLOWED_HOSTS = ["*"]

# ================================================
# ================================================
# PATHS 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
FRONTEND_DIR  = os.path.join(BASE_DIR, "frontend")

# ================================================
# ================================================
# AUTH 

LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "/"

SITE_ID = 1

# ================================================
# ================================================
# APP 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    "django.contrib.contenttypes",
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_registration",
    "rest_framework",
    "invitations",
    "django_filters",
    "django_extensions",
    "webpack_loader",
    "cartographer",
    "api",
    "user_administration",
    "closed",
    "consent",
    "unsubscribe",
    #"mocking",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "closed.middleware.check_active",
    "consent.middleware.has_consented"
]

ROOT_URLCONF = 'conflictcartographer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'conflictcartographer.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ================================================
# ================================================
# REST framework 

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

# ================================================
# ================================================
# EMAIL STUFF 

SENDGRID_API_KEY   = env.str("EMAIL_API_KEY",      "")
EMAIL_FROM_ADDRESS = env.str("EMAIL_FROM_ADDRESS", "conflictcartographer@prio.org")
DEFAULT_FROM_EMAIL = env.str("EMAIL_FROM_ADDRESS", EMAIL_FROM_ADDRESS)

if not DEBUG and SENDGRID_API_KEY:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_INTERVAL = 1

DEFAULT_EMAIL_TITLE             = "Invitation to participate in an expert survey"
DEFAULT_PLAINTEXT_MAIL_TEMPLATE = "mail/invitation.txt"
DEFAULT_HTML_MAIL_TEMPLATE      = "mail/invitation.html"

PUBLIC_URL           = "http://0.0.0.0:8000" if DEBUG else "https://conflictcartographer.prio.org"
INVITATION_LINK_BASE = os.path.join(PUBLIC_URL,"accounts","ref")
UNSUB_LINK_BASE      = os.path.join(PUBLIC_URL,"accounts","unsub")

# EMAIL RENDERING

EMAIL_HEAD  = os.path.join(BASE_DIR,"email","head.html")
EMAIL_TAIL  = os.path.join(BASE_DIR,"email","tail.html")
EMAIL_STYLE = os.path.join(BASE_DIR,"email","style.css")

# ================================================
# ================================================
# APP 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    "formatters": {
        "standard":{
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,"logs/app.log"),
            "maxBytes": 1024*1024*5, # 5 MiB
            "backupCount": 5,
            "formatter": "standard",
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,"logs/app.request.log"),
            "maxBytes": 1024*1024*5, # 5 MiB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    'loggers': {
        '': {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            "min_length": 13
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ================================================
# ================================================
# STATIC 

if env.bool("DEFAULT_STATIC", False):
    STATIC_URL = "/static/"
else:
    if DEBUG:
        STATIC_HOST = 'http://0.0.0.0:1337' if DEBUG else ''
    else:
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
        STATIC_ROOT = os.path.join(BASE_DIR,"static")
        STATIC_HOST=""
    STATIC_URL = STATIC_HOST + "/static/" 

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR,"compiled")
        ]

    DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880


# ================================================
# ================================================
# SERVICES 

SCHEDULE_FRAC = env.int("SCHEDULE_FRAC", 4)
OPEN_MONTHS   = env.int("OPEN_MONTHS",   3)

SCHEDULER_URL = env.str("SCHEDULER_URL", "http://scheduler")
METRICS_URL   = env.str("METRICS_URL",   "http://metrics")
API_URL       = env.str("API_URL",       "http://api")
GED_URL       = env.str("GED_URL",       "http://ged")


# ================================================
# ================================================
# DATA MOCKING

MOCK_N_USERS = env.int("MOCK_N_USERS", 100)
MOCK_MAX_PREDICTIONS_PER_USER_COUNTRY = env.int("MOCK_MAX_PREDICTIONS_PER_USER_COUNTRY", 20)
MOCK_USER_PASSWORD = env.str("MOCK_USER_PASSWORD", "iamjustamockuser")
