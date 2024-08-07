from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from contracts.models import Contract
from clients.models import Client
from contracts.filters import (ClientFilter, SupplierFilter, UtilityTypeFilter,
                               MultiStatusFilter, )
from rangefilter.filters import DateRangeFilter
from contacts.models import Contact, JobTitle
from commissions.models import ElectricityCommission, GasCommission
from utilities.models import Supplier, Utility
from contracts.admin_actions import bulk_quote_template
from core.decorators import admin_changelist_link
from .resources import ClientResource, ContactResource
from contracts.custom_search import CustomSearchAdmin


class AccountManagerAdminSite(AdminSite):
    site_header = "Energy Portfolio Account Manager Portal"
    site_title = "Account Manager Admin"
    index_title = "Welcome to Energy Portfolio Account Manager Portal"


account_manager_admin = AccountManagerAdminSite(name='account_manager_admin')


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1  # Number of empty forms to display


class ElectricityCommissionInline(admin.TabularInline):
    model = ElectricityCommission
    extra = 0


class GasCommissionInline(admin.TabularInline):
    model = GasCommission
    extra = 0


class SupplierAdmin(admin.ModelAdmin):
    list_display = ("supplier", "meter_email", "suppliers_link")
    list_filter = ("supplier",)
    search_fields = ('supplier',)
    ordering = ("supplier",)

    @admin_changelist_link(
        "contract_suppliers", _("All Contracts"), query_string=lambda c: f"supplier_id={c.pk}"
    )
    def suppliers_link(self, contract_suppliers):
        return _("All Contracts")


account_manager_admin.register(Supplier, SupplierAdmin)


class UtilityAdmin(admin.ModelAdmin):
    search_fields = ('utility',)


account_manager_admin.register(Utility, UtilityAdmin)

class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ContactResource
    list_display = ("name", "email", "client", "job_title")
    list_filter = (
        "client",
        "name",
        "email",
        "phone_number",
    )
    autocomplete_fields = ("client",)
    search_fields = ("name", "email", "client__client")


account_manager_admin.register(Contact, ContactAdmin)


class JobTitleAdmin(admin.ModelAdmin):
    inlines = (ContactInline,)


account_manager_admin.register(JobTitle, JobTitleAdmin)
class ClientAdmin(ExportActionMixin, admin.ModelAdmin):
    show_full_result_count = False
    inlines = [ContactInline, ElectricityCommissionInline, GasCommissionInline]
    readonly_fields = ['is_lost', 'client_lost_date', 'contracts_link']
    resource_class = ClientResource
    list_per_page = 10
    list_display = (
        "id",
        "client",
        "account_manager",
        "originator",
        "client_onboarded",
        "is_lost",
        "client_lost_date",
        "loa",
        "contracts_link",
    )
    list_filter = ('client', 'account_manager', "is_lost")
    search_fields = ('client',)
    ordering = ("client",)

    @admin_changelist_link(
        "client_contracts", _("All Contracts"), query_string=lambda c: f"client_id={c.pk}"
    )
    def contracts_link(self, client_contracts):
        return _("All Contracts")


account_manager_admin.register(Client, ClientAdmin)


class ContractAdmin(ExportActionMixin, CustomSearchAdmin, admin.ModelAdmin):
    readonly_fields = [field.name for field in Contract._meta.fields if field.name != 'notes']

    def has_change_permission(self, request, obj=None):
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []

    list_per_page = 10
    ordering = ("id",)
    list_display = (
        "id",
        "client",
        "client_group",
        "contract_status",
        "business_name",
        "contract_type",
        "seamless_updated",
        "client_manager",
        "site_address",
        "supplier",
        "utility",
        "meter_serial_number",
        "mpan_mpr",
        "eac",
        "commission_per_annum",
        "commission_per_unit",
        "contract_start_date",
        "contract_end_date",
        "is_ooc",
        "is_directors_approval",
    )
    fieldsets = (
        (
            "Site Information",
            {
                "description": "Enter the site details",
                "fields": (
                    ("client", "client_group", "business_name", "client_manager"),
                    "site_address",
                    "supplier",
                    "utility",
                    "mpan_mpr",
                    "meter_serial_number",
                    "meter_status",
                    "smart_meter",
                    "top_line",
                    "vat_rate",
                    "vat_declaration_sent",
                    "vat_declaration_date",
                    "vat_declaration_expires",
                ),
            },
        ),
        (
            "Contract Information",
            {
                "description": "Contract Information",
                "fields": (
                    (
                        "account_number",
                        "company_reg_number",
                    ),
                    "is_directors_approval",
                    "directors_approval_date",
                    "contract_type",
                    "contract_status",
                    "meter_onboarded",
                ),
            },
        ),
        (
            "Contract Date Details",
            {
                "description": "Enter the following details",
                "fields": (
                    (
                        "contract_start_date",
                        "contract_end_date",
                        "supplier_start_date",
                        "lock_in_date",
                    ),
                    "is_ooc",
                ),
            },
        ),
        (
            "Seamless Contract Information",
            {
                "description": "The following only applies to seamless contracts",
                "fields": (
                    ("supplier_coding",),
                    ("building_name", "billing_address"),
                    ("day_consumption", "night_consumption", "contract_value"),
                    ("standing_charge", "sc_frequency"),
                    ("unit_rate_1", "unit_rate_2", "unit_rate_3"),
                    "seamless_status",
                    "seamless_updated",
                ),
            },
        ),
        (
            "Service Information",
            {
                "description": "Enter the following data",
                "fields": (
                    "eac",
                    "profile",
                    "service_type",
                    "feed_in_tariff",
                    "kva",
                ),
            },
        ),
        (
            "Rates",
            {
                "description": "Enter the following data",
                "fields": (
                    "pence_per_kilowatt",
                    "day_kilowatt_hour_rate",
                    "night_rate",
                    "annualised_budget",
                ),
            },
        ),
        (
            "Commissions",
            {
                "description": "Enter the following",
                "fields": (
                    "commission_per_annum",
                    "commission_per_unit",
                    "partner_commission",
                ),
            },
        ),
        ("Notes", {"description": "Additional Information", "fields": ("notes",)}),
    )
    list_filter = ("contract_type", MultiStatusFilter, ClientFilter, SupplierFilter, UtilityTypeFilter, "is_ooc",
                   "is_directors_approval", ("contract_end_date", DateRangeFilter),
                   ("contract_start_date", DateRangeFilter), "meter_status", "vat_rate",)
    search_fields = (
        "business_name",
        "client__client",
        "client_group",
        "utility__utility",
        "supplier__supplier",
        "mpan_mpr",
        "meter_serial_number",
        "site_address",
    )
    actions = [
        bulk_quote_template,
    ]


account_manager_admin.register(Contract, ContractAdmin)
