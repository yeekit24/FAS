"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import REST_FRAMEWORK, env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "APP_UID",
    default="TSumE3hniL3BQcsx8K7bhpHQ3yKadC9XrkhQ6LqUSa0yAHDxSmPEtpyr5vdGon9P",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"
TESTING_TOKEN = env.str(
    "TESTING_TOKEN", "Bearer ef47783524afa4afc75601ee51d73ab1af244238"
)
TESTING_TOKEN_USER_ID = env.int("TESTING_TOKEN_USER_ID", 2)

# TODO: Using PostgreSQL means we can unit test the database used in producion, but it also means
# that to run a unit test, there must be a running PostgreSQL service. Also, it seems to come with
# issues with cursor. Explore the possibility of just using SQLite. It will make the tests run
# faster (as there's no need to run a PostgreSQL service), and be executed in different environments
# e.g. as part of GitHub actions during a pull request.
# Database
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#     }
# }

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# Permission
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "rest_framework.permissions.IsAuthenticated"
]

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]
