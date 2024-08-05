from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from django import forms
from django.contrib import messages

from .models import Client
from core.decorators import admin_changelist_link

from commissions.models import ElectricityCommission, GasCommission

User = get_user_model()


class ClientAdminForm(forms.ModelForm):
    confirm_export = forms.BooleanField(
        required=False, label="You must confirm you have exported all the contracts"
    )

    class Meta:
        model = Client
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        is_lost = cleaned_data.get("is_lost")
        confirm_export = cleaned_data.get("confirm_export")

        if is_lost and not self.instance.is_lost and not confirm_export:
            raise forms.ValidationError(
                "Please export all relevant contracts and confirm you have exported the contracts"
                " before marking this client as lost."
            )

        return cleaned_data


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
            "client_lost_date",
        ]
        import_id_fields = ["id"]

        export_order = (
            "id",
            "client",
            "account_manager",
            "contract_term",
            "originator",
            "client_onboarded",
            "loa",
            "is_lost",
            "client_lost_date",
        )


class ClientAdmin(ImportExportModelAdmin):
    show_full_result_count = False
    form = ClientAdminForm
    resource_class = ClientResource
    inlines = [ElectricityCommissionInline, GasCommissionInline]
    list_display = (
        "id",
        "client",
        "contract_term",
        "originator",
        "client_onboarded",
        "is_lost",
        "client_lost_date",
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
    fieldsets = (
        (
            "Client Information",
            {
                "description": "Enter the Client details",
                "fields": (
                    ("client", "account_manager"),
                    ("originator", "client_onboarded"),
                    ("loa", "contract_term"),
                    "notes",
                ),
            },
        ),
        (
            "Lost Client Information",
            {
                "description": "",
                "fields": (
                    (
                        "is_lost",
                        "confirm_export",
                    ),
                ),
            },
        ),
        (
            "Lost Client Audit Information",
            {
                "description": "These are information fields only and are automatically system generated",
                "fields": (("client_lost_date", "export_confirmed"),),
            },
        ),
    )
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

    def save_model(self, request, obj, form, change):
        if obj.is_lost and not Client.objects.get(id=obj.id).is_lost:
            if form.cleaned_data.get("confirm_export"):
                obj.export_confirmed = True
                self.message_user(
                    request,
                    "Client marked as lost. Contracts export confirmed.",
                    level=messages.SUCCESS,
                )
            else:
                self.message_user(
                    request,
                    "Please confirm the contracts export before marking the client as lost.",
                    level=messages.ERROR,
                )
                return
        super().save_model(request, obj, form, change)


admin.site.register(Client, ClientAdmin)
