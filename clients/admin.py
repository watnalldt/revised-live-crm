from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Client
from core.decorators import admin_changelist_link

from commissions.models import ElectricityCommission, GasCommission

User = get_user_model()


class ElectricityCommissionResource(resources.ModelResource):
    class Meta:
        model = ElectricityCommission


class ElectricityCommissionInline(admin.TabularInline):
    model = ElectricityCommission
    extra = 1


class GasCommissionInline(admin.TabularInline):
    model = GasCommission
    extra = 1


class ClientResource(resources.ModelResource):
    account_manager = fields.Field(
        column_name="account_manager",
        attribute="account_manager",
        widget=ForeignKeyWidget(User, "email"),
    )
    client__electricity_commission =                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Field(
        attribute="electricity_commission", column_name="Electricity Commission"
    )

    class Meta:
        model = Client
        skip_unchanged = True
        report_skipped = True
        fields = [
            "id",
            "client",
            "account_manager",
            "contract_term",
            "originator",
            "client_onboarded",
            "loa",
            "is_lost",
        ]
        import_id_fields = ["id"]

        export_order = [
            "id",
            "client",
            "account_manager",
            "contract_term",
            "originator",
            "client_onboarded",
            "loa",
            "is_lost",
            "client__electricity_commission",
        ]


class ClientAdmin(ImportExportModelAdmin):
    show_full_result_count = False
    resource_class = ClientResource
    inlines = [ElectricityCommissionInline, GasCommissionInline]
    list_display = (
        "id",
        "client",
        "contract_term",
        "originator",
        "client_onboarded",
        "is_lost",
        "loa",
        "link_to_account_managers",
        "contracts_link",
    )
    list_filter = (
        "client",
        "is_lost",
        "account_manager",
    )
    list_select_related = ("account_manager",)
    autocomplete_fields = ("account_manager",)
    search_fields = ("client", "account_manager__email")
    list_per_page = 25
    search_help_text = "Search by Client Name"
    ordering = ("client",)

    @admin_changelist_link(
        "client_contracts", _("All Contracts"), query_string=lambda c: f"client_id={c.pk}"
    )
    def contracts_link(self, client_contracts):
        return _("All Contracts")

    def link_to_account_managers(self, obj):
        link = reverse("admin:users_accountmanager_change", args=[obj.account_manager.id])
        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.account_manager,
        )

    link_to_account_managers.short_description = "Account Managers"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Check if the user belongs to the specific group
        if not request.user.groups.filter(name="ContractAdmins").exists():
            # If the user is not in the group, hide the 'is_lost' field
            if "is_lost" in form.base_fields:
                form.base_fields.pop("is_lost")

        return form


admin.site.register(Client, ClientAdmin)
