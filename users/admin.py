from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from core.decorators import admin_changelist_link

from .models import AccountManager, ClientManager, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ["email"]


class CustomUserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password", "role", "last_login")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = (
        "email",
        "first_name",
        "is_staff",
        "is_active",
        "last_login",
        "role",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
        "role",
    )
    search_fields = ("email",)
    search_help_text = "Enter user's email"
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, CustomUserAdmin)


class AccountManagerAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "clients_link",
    )
    search_fields = ("email",)

    @admin_changelist_link(
        "account_manager_clients",
        _("All Clients"),
        query_string=lambda c: f"account_manager_id={c.pk}",
    )
    def clients_link(self, account_manager_clients):
        return _("All Clients")


admin.site.register(AccountManager, AccountManagerAdmin)


class ClientManagerAdmin(admin.ModelAdmin):
    list_display = ("email",)
    search_fields = ("email",)


admin.site.register(ClientManager, ClientManagerAdmin)
