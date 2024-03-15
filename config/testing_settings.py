from .settings import *  # noqa

# An in-memory database should be good enough for now.

# Make sure that tests are never sending real emails.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
