from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.utils.html import format_html


def client_manager_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="/users/login"
):
    """
    Decorator for views that checks that the user logging in is a client manager,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == "CLIENT_MANAGER",
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    return actual_decorator(function) if function else actual_decorator


def account_manager_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="/users/login/"
):
    """
    Decorator for views that checks that the user logging in is an account manager,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.role == "ACCOUNT_MANAGER",
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    return actual_decorator(function) if function else actual_decorator


def admin_changelist_url(model):
    app_label = model._meta.app_label
    model_name = model.__name__.lower()
    return reverse(f"admin:{app_label}_{model_name}_changelist")


def admin_changelist_link(attr, short_description, empty_description="-", query_string=None):
    def wrap(func):
        def field_func(self, obj):
            related_obj = getattr(obj, attr)
            if related_obj is None:
                return empty_description
            url = admin_changelist_url(related_obj.model)
            if query_string:
                url += "?" + query_string(obj)
            return format_html('<a href="{}">{}</a>', url, func(self, related_obj))

        field_func.short_description = short_description
        field_func.allow_tags = True
        return field_func

    return wrap
