from .settings import *  # noqa


# Make sure that tests are never sending real emails.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
