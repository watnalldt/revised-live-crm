from django.contrib import admin
from django.contrib.admin import AdminSite
from clients.models import Client
from contracts.models import Contract
from django.utils.translation import gettext_lazy as _
from core.decorators import admin_changelist_link
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
import tablib
from django.http import HttpResponse
from contacts.models import JobTitle, Contact
from utilities.models import Supplier, Utility
from django.db.models import Q
from admin_auto_filters.filters import AutocompleteFilter
from rangefilter.filters import DateRangeFilter
from core.decorators import admin_changelist_link
from commissions.models import ElectricityCommission, GasCommission
from django.forms import forms


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


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        export_order = (
            "id",
            "client",
            "originator",
            "client_onboarded",
            "loa",
            "is_lost",
        )


class ClientAdmin(ExportActionMixin, admin.ModelAdmin):
    show_full_result_count = False
    inlines = [ContactInline, ElectricityCommissionInline, GasCommissionInline]
    readonly_fields = ['is_lost', 'client_lost_date']
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


class ContactResource(resources.ModelResource):
    Client = fields.Field(
        column_name="client",
        attribute="client",
        widget=ForeignKeyWidget(Client, "client"),
    )

    JobTitle = fields.Field(
        column_name="job_title",
        attribute="job_title",
        widget=ForeignKeyWidget(JobTitle, "title"),
    )

    class Meta:
        model = Contact
        skip_unchanged = True
        report_skipped = True
        fields = ["id", "name", "email", "phone_number"]
        import_id_fields = ["id"]

        export_order = [
            "id",
            "name",
            "email",
            "phone_number",
        ]


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


class ClientFilter(AutocompleteFilter):
    title = "Client"  # display title
    field_name = "client"  # name of the foreign key field


class SupplierFilter(AutocompleteFilter):
    title = "Supplier"  # display title
    field_name = "supplier"  # name of the foreign key field


class UtilityTypeFilter(AutocompleteFilter):
    title = "Utility Type"  # display title
    field_name = "utility"  # name of the foreign key field


class MultiStatusFilter(admin.SimpleListFilter):
    title = _("Contract Status")  # Human-readable title which will be displayed
    parameter_name = "contract_status"  # URL parameter name for filtering

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. Each tuple contains a value and its corresponding
        human-readable name to be displayed in the admin filter sidebar.
        """
        # Assuming Contract.ContractStatus is a list or an enum-like of statuses; adapt if it's structured differently
        return [(status.value, status.name) for status in Contract.ContractStatus]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value(s) provided in the query string
        which are retrievable via `self.value()`. Supports multiple selections.
        """
        if self.value():
            # Splitting the values on commas allows for multiple statuses to be filtered
            filter_values = self.value().split(",")
            return queryset.filter(contract_status__in=filter_values)
        return queryset


class ContractResource(resources.ModelResource):
    client = fields.Field(
        column_name="client", attribute="client", widget=ForeignKeyWidget(Client, "client")
    )
    supplier = fields.Field(
        column_name="supplier", attribute="supplier", widget=ForeignKeyWidget(Supplier, "supplier")
    )
    utility = fields.Field(
        column_name="utility", attribute="utility", widget=ForeignKeyWidget(Utility, "utility")
    )

    class Meta:
        model = Contract
        export_order = (
            "id",
            "contract_type",
            "seamless_updated",
            "contract_status",
            "client",
            "client_group",
            "is_directors_approval",
            "directors_approval_date",
            "business_name",
            "company_reg_number",
            "utility",
            "top_line",
            "mpan_mpr",
            "meter_serial_number",
            "meter_onboarded",
            "meter_status",
            "building_name",
            "site_address",
            "billing_address",
            "supplier",
            "supplier_coding",
            "contract_start_date",
            "contract_end_date",
            "lock_in_date",
            "supplier_start_date",
            "account_number",
            "eac",
            "day_consumption",
            "night_consumption",
            "vat_rate",
            "contract_value",
            "standing_charge",
            "sc_frequency",
            "unit_rate_1",
            "unit_rate_2",
            "unit_rate_3",
            "feed_in_tariff",
            "seamless_status",
            "profile",
            "is_ooc",
            "service_type",
            "pence_per_kilowatt",
            "day_kilowatt_hour_rate",
            "night_rate",
            "annualised_budget",
            "commission_per_annum",
            "commission_per_unit",
            "commission_per_contract",
            "partner_commission",
            "smart_meter",
            "vat_declaration_sent",
            "vat_declaration_date",
            "vat_declaration_expires",
            "notes",
            "kva",
        )


class ContractAdmin(ExportActionMixin, admin.ModelAdmin):
    readonly_fields = [field.name for field in Contract._meta.fields if field.name != 'notes']

    def has_change_permission(self, request, obj=None):
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []

    show_full_result_count = False
    resource_class = ContractResource
    date_hierarchy = 'contract_end_date'
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
        "bulk_quote_template",
    ]

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

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.client.account_manager != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.client.account_manager != request.user:
            return False
        return super().has_delete_permission(request, obj)

    def bulk_quote_template(self, request, queryset):
        # Specify the fields you want to export
        fields_to_export = [
            "id",
            "client",
            "billing_address",
            "company_reg_number",
            "business_name",
            "site_address",
            "top_line",
            "mpan_mpr",
            "supplier",
            "contract_type",
            "contract_status",
            "contract_end_date",
            "eac",
            "is_directors_approval",
            "commission_per_annum",
            "commission_per_unit",
            "vat_rate",
        ]

        data = tablib.Dataset()
        data.headers = fields_to_export

        for obj in queryset:
            row = []
            for field in fields_to_export:
                value = getattr(obj, field)

                if field == "contract_end_date":
                    if value:
                        value = value.strftime("%d/%m/%Y")  # Format date to UK format
                    else:
                        value = ""
                elif field == "commission_per_unit":
                    if value not in [0.01, 0.02, 0.03]:
                        value = round(value * 100, 2)

                row.append(value)

            data.append(row)

        response = HttpResponse(data.export("xlsx"), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="bulk_quote_template.xlsx"'
        return response

    bulk_quote_template.short_description = "Bulk Quote Template"

    def get_search_results(self, request, queryset, search_term):
        """
        Enhances filtering by allowing searches for multiple MPAN numbers separated by commas,
        and maintains compatibility with other applied filters.
        """
        use_distinct = False

        # Check if the search_term involves potential multiple MPAN numbers
        if "," in search_term:
            mpan_terms = [term.strip() for term in search_term.split(",") if term.strip()]
            if mpan_terms:
                q_objects = Q(mpan_mpr__iexact=mpan_terms[0])  # Start with the first term
                for term in mpan_terms[1:]:
                    q_objects |= Q(mpan_mpr__iexact=term)  # Use |= to add each subsequent term

                queryset = queryset.filter(q_objects).distinct()
                use_distinct = True
        else:
            # Handle single mpan_mpr or other search fields via superclass method
            queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        return queryset, use_distinct


account_manager_admin.register(Contract, ContractAdmin)
