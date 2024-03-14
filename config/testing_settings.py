from .settings import *  # noqa

# An in-memory database should be good enough for now.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# Make sure that tests are never sending real emails.
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
