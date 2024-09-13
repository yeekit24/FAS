"""Base settings to build other settings files upon.

Notes
-----
FIXME: fields.W904
django-stubs==1.5.0 currently does not support `models.JSONField`.
Using the deprecated `contrib.postgres.fields.JSONField` for now.
https://github.com/typeddjango/django-stubs/issues/439

"""
from pathlib import Path
from django.urls import reverse_lazy

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = ROOT_DIR / "src"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", True)
TIME_ZONE = "Asia/Singapore"
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = True
SILENCED_SYSTEM_CHECKS = [
    "fields.W904",  # See docstring for more info
]

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://fas_user:@localhost:5432/fas_db"
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "health_check",
    "health_check.db",
    "jsoneditor",
    "drf_yasg",
    "auditlog",
]

LOCAL_APPS = [
    "src.authentication.apps.AuthenticationConfig",
    "src.applicants.apps.ApplicantsConfig",
    "src.applications.apps.ApplicationsConfig",
    "src.schemes.apps.SchemesConfig",
    "src.common.apps.CommonConfig",
    "src.users.apps.UsersConfig",
    "src.specs.apps.SpecsConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
AUTH_USER_MODEL = "users.User"

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=str(ROOT_DIR / "staticfiles"))
STATIC_URL = env.str("DJANGO_STATIC_URL", default="/static/")
# STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                # "django.template.context_processors.i18n",
                # "django.template.context_processors.media",
                # "django.template.context_processors.static",
                # "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

APP_UID = env.str("APP_UID", default="travelpeta")

# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
# CSRF_TRUSTED_ORIGINS = [""]
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = env.str("DJANGO_ADMIN_URL", "admin/")
ADMINS = [("FAS", "dev@fas.com")]
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
        "src": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "src.authentication.token_bearer.TokenBearerAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "EXCEPTION_HANDLER": "src.utils.exception_handlers.exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Django IPware
# -------------------------------------------------------------------------------
# django-ipware - https://github.com/un33k/django-ipware
IPWARE_META_PRECEDENCE_ORDER = (
    # https://support.cloudflare.com/hc/en-us/articles/200170986-How-does-Cloudflare-handle-HTTP-Request-headers-
    "HTTP_CF_CONNECTING_IP",
    "HTTP_X_FORWARDED_FOR",
    "X_FORWARDED_FOR",  # <client>, <proxy1>, <proxy2>
    "HTTP_CLIENT_IP",
    "HTTP_X_REAL_IP",
    "HTTP_X_FORWARDED",
    "HTTP_X_CLUSTER_CLIENT_IP",
    "HTTP_FORWARDED_FOR",
    "HTTP_FORWARDED",
    "HTTP_VIA",
    "REMOTE_ADDR",
)

# configuration
# ------------------------------------------------------------------------------
#


# Queue configuration (Faust App)
# ------------------------------------------------------------------------------
# Kafka settings
QUEUE_BROKER = env.list("QUEUE_BROKER", default=["kafka://kafka:9092"])
QUEUE_DS_TOPIC = env.str("QUEUE_DS_TOPIC", default="data_source_topic")
QUEUE_STORE = env.str("QUEUE_STORE", default="memory://")

# SSL and Cert settings only used if SSL is enabled.
QUEUE_ENABLE_SSL = env.bool("QUEUE_ENABLE_SSL", False)
QUEUE_ENABLE_SSL_HOSTNAME_CHECK = env.bool("QUEUE_ENABLE_SSL_HOSTNAME_CHECK", False)
QUEUE_ENABLE_SSL_VERIFY = env.bool("QUEUE_ENABLE_SSL_VERIFY", True)
# Path to root CA cert in PEM format, if required.
QUEUE_SSL_CA = env.str("QUEUE_SSL_CA", None)
# Path to cert & key chain in PEM format, if required
QUEUE_CERT_CHAIN = env.str("QUEUE_CERT_CHAIN", "")
QUEUE_CERT_CHAIN_PASSWORD = env.str("QUEUE_CERT_CHAIN_PASSWORD", "")

# Bucket settings
S3_DOCKER_ENDPOINT_URL = env.str("S3_DOCKER_ENDPOINT_URL", default=None)
S3_ENDPOINT_URL = env.str("S3_ENDPOINT_URL", default=None)
S3_BUCKET = env.str("S3_BUCKET", default="")
S3_ACCESS_KEY = env.str("S3_ACCESS_KEY", default=None)
S3_SECRET_KEY = env.str("S3_SECRET_KEY", default=None)
S3_EXPIRATION = env.str("S3_EXPIRATION", default=3600)

# JSONEditor configuration
# ------------------------------------------------------------------------------
JSON_EDITOR_ACE_OPTIONS_JS = "ace_options.js"
JSON_EDITOR_INIT_JS = "jsoneditor-init.js"


# Session token lifetime in second (default 15 min)
SESSION_TOKEN_LIFETIME = env.str("SESSION_TOKEN_LIFETIME", 900)

# drf-yasg
# -------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    "LOGIN_URL": reverse_lazy("admin:login"),
    "LOGOUT_URL": "/admin/logout",
    "PERSIST_AUTH": True,
    "REFETCH_SCHEMA_WITH_AUTH": True,
    "REFETCH_SCHEMA_ON_LOGOUT": True,
    "DEFAULT_INFO": "src.specs.urls.swagger_info",
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "in": "header",
            "name": "Authorization",
            "type": "apiKey",
        },
    },
}
