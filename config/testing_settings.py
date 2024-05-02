from .settings import *  # noqa


# Make sure that tests are never sending real emails.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
