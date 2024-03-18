import openpyxl
import tablib
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.db.models import Count, ExpressionWrapper, F, FloatField, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from rangefilter.filters import DateRangeFilter

from clients.models import Client
from utilities.models import Supplier, Utility

from .models import Contract

User = get_user_model()


class ClientFilter(AutocompleteFilter):
    title = "Client"  # display title
    field_name = "client"  # name of the foreign key field


class ClientManagerFilter(AutocompleteFilter):
    title = "Client Manager"  # display title
    field_name = "client_manager"  # name of the foreign key field


class SupplierFilter(AutocompleteFilter):
    title = "Supplier"  # display title
    field_name = "supplier"  # name of the foreign key field


class UtilityTypeFilter(AutocompleteFilter):
    title = "Utility Type"  # display title
    field_name = "utility"  # name of the foreign key field


class FutureSupplierFilter(AutocompleteFilter):
    title = "Future Supplier"  # display title
    field_name = "future_supplier"  # name of the foreign key field


class ContractResource(resources.ModelResource):
    client = fields.Field(
        column_name="client", attribute="client", widget=ForeignKeyWidget(Client, "client")
    )
    client_manager = fields.Field(
        column_name="client_manager",
        attribute="client_manager",
        widget=ForeignKeyWidget(User, "email"),
    )
    supplier = fields.Field(
        column_name="supplier", attribute="supplier", widget=ForeignKeyWidget(Supplier, "supplier")
    )
    utility = fields.Field(
        column_name="utility", attribute="utility", widget=ForeignKeyWidget(Utility, "utility")
    )

    class Meta:
        model = Contract

        report_skipped = True
        import_id_fields = ("id",)
        export_order = [
            "id",
            "client",
            "client_group",
            "business_name",
            "site_address",
            "client_manager",
            "supplier",
            "utility",
            "mpan_mpr",
            "meter_serial_number",
            "meter_status",
            "smart_meter",
            "top_line",
            "account_number",
            "company_reg_number",
            "building_name",
            "billing_address",
            "is_directors_approval",
            "contract_type",
            "contract_status",
            "meter_onboarded",
            "vat_rate",
            "vat_declaration_sent",
            "vat_declaration_date",
            "vat_declaration_expires",
            "lock_in_date",
            "contract_start_date",
            "contract_end_date",
            "supplier_start_date",
            "is_ooc",
            "pence_per_kilowatt",
            "day_kilowatt_hour_rate",
            "night_rate",
            "annualised_budget",
            "day_consumption",
            "night_consumption",
            "contract_value",
            "standing_charge",
            "sc_frequency",
            "unit_rate_1",
            "unit_rate_2",
            "unit_rate_3",
            "supplier_coding",
            "seamless_status",
            "seamless_updated",
            "eac",
            "profile",
            "service_type",
            "feed_in_tariff",
            "kva",
            "commission_per_annum",
            "commission_per_unit",
            "commission_per_contract",
            "partner_commission",
            "notes",
        ]


class ContractFilter(admin.SimpleListFilter):
    title = "5% Vat no declaration"
    parameter_name = "contracts"

    def lookups(self, request, model_admin):
        return (("relevant_contracts", "Contracts 5% VAT no vat declaration"),)

    def queryset(self, request, queryset):
        if self.value() == "relevant_contracts":
            seven_days_ago = timezone.now() - timezone.timedelta(days=7)
            return queryset.filter(
                contract_start_date__lt=seven_days_ago, vat_rate="5%", vat_declaration_sent="NO"
            )


class SevenDaysAgoFilter(admin.SimpleListFilter):
    title = "Start Date More Than 7 Days Ago"
    parameter_name = "start_date_7_days_ago"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            seven_days_ago = timezone.now() - timezone.timedelta(days=7)
            return queryset.filter(contract_start_date__lt=seven_days_ago)
        elif self.value() == "no":
            seven_days_ago = timezone.now() - timezone.timedelta(days=7)
            return queryset.exclude(contract_start_date__lt=seven_days_ago)
        return queryset


class StartDateIsNullFilter(admin.SimpleListFilter):
    title = _("Start Date Is Empty")
    parameter_name = "start_date_is_null"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(contract_start_date__isnull=True)
        elif self.value() == "no":
            return queryset.filter(contract_start_date__isnull=False)


class ContractAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    show_full_result_count = False
    resource_class = ContractResource
    list_per_page = 10
    ordering = ("id",)
    readonly_fields = ("commission_per_annum", "commission_per_unit")
    list_display = (
        "id",
        "contract_status",
        "business_name",
        "contract_type",
        "seamless_updated",
        "link_to_clients",
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
    list_display_links = ("business_name",)
    list_select_related = ("client", "client_manager", "supplier", "utility")
    fieldsets = (
        (
            "Site Information",
            {
                "description": "Enter the site details",
                "fields": (
                    (
                        "client",
                        "client_group",
                    ),
                    "business_name",
                    "site_address",
                    "client_manager",
                    "supplier",
                    "utility",
                    "mpan_mpr",
                    "meter_serial_number",
                    "meter_status",
                    "smart_meter",
                    "top_line",
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
                    ("building_name", "billing_address"),
                    "is_directors_approval",
                    "contract_type",
                    "contract_status",
                    "meter_onboarded",
                ),
            },
        ),
        (
            "VAT Information",
            {
                "fields": (
                    "vat_rate",
                    "vat_declaration_sent",
                    "vat_declaration_date",
                    "vat_declaration_expires",
                )
            },
        ),
        (
            "Contract Date and Contract Rates",
            {
                "description": "Enter the following details",
                "fields": (
                    (
                        "lock_in_date",
                        "contract_start_date",
                        "contract_end_date",
                    ),
                    (
                        "supplier_start_date",
                        "is_ooc",
                    ),
                    (
                        "pence_per_kilowatt",
                        "day_kilowatt_hour_rate",
                        "night_rate",
                        "annualised_budget",
                    ),
                    ("day_consumption", "night_consumption", "contract_value"),
                    ("standing_charge", "sc_frequency"),
                    ("unit_rate_1", "unit_rate_2", "unit_rate_3"),
                ),
            },
        ),
        (
            "Seamless Contract Information",
            {
                "description": "The following only applies to seamless contracts",
                "fields": (
                    ("supplier_coding",),
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
            "Commissions",
            {
                "description": "Commissions are applied at client level",
                "fields": (
                    "commission_per_annum",
                    "commission_per_unit",
                    "commission_per_contract",
                    "partner_commission",
                ),
            },
        ),
        ("Notes", {"description": "Additional Information", "fields": ("notes",)}),
    )
    list_filter = [
        "contract_type",
        "seamless_updated",
        "contract_status",
        ClientFilter,
        "client_group",
        ClientManagerFilter,
        SupplierFilter,
        UtilityTypeFilter,
        "seamless_status",
        "is_ooc",
        "is_directors_approval",
        ("contract_end_date", DateRangeFilter),
        ("contract_start_date", DateRangeFilter),
        "vat_rate",
        "vat_declaration_sent",
        StartDateIsNullFilter,
        ContractFilter,
        "meter_status",
    ]
    autocomplete_fields = [
        "client",
        "client_manager",
        "supplier",
    ]
    search_help_text = "Search by MPAN/MPR or Business Name, Client Name, Meter Serial Number"
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
    date_hierarchy = "contract_end_date"

    actions = [
        "directors_approval_not_required",
        "directors_approval_required",
        "contracts_lost",
        "change_contract_to_seamless",
        "change_contract_to_non_seamless",
        "make_contract_live",
        "make_contract_pricing",
        "make_contract_objection",
        "make_contract_locked",
        "out_of_contract",
        "bulk_quote_template",
        "change_vat_rate_to_5_percent",
        "change_vat_rate_to_20_percent",
        "seamless_contract_updated",
        "seamless_contract_not_updated",
        "export_commissions_to_excel",
    ]

    @admin.action(description="Directors Approval Not Required")
    def directors_approval_not_required(self, request, queryset):
        queryset.update(is_directors_approval="NO")

    @admin.action(description="Directors Approval Required")
    def directors_approval_required(self, request, queryset):
        queryset.update(is_directors_approval="YES")

    @admin.action(description="Seamless Contract Updated")
    def seamless_contract_updated(self, request, queryset):
        queryset.update(seamless_updated="YES")

    @admin.action(description="Seamless Contract Not Updated")
    def seamless_contract_not_updated(self, request, queryset):
        queryset.update(seamless_updated="NO")

    @admin.action(description="Make Out of Contract")
    def out_of_contract(self, request, queryset):
        queryset.update(is_ooc="YES")

    @admin.action(description="Make Live")
    def make_contract_live(self, request, queryset):
        queryset.update(contract_status="LIVE")

    @admin.action(description="Pricing")
    def make_contract_pricing(self, request, queryset):
        queryset.update(contract_status="PRICING")

    @admin.action(description="Objection")
    def make_contract_objection(self, request, queryset):
        queryset.update(contract_status="OBJECTION")

    @admin.action(description="Locked")
    def make_contract_locked(self, request, queryset):
        queryset.update(contract_status="LOCKED")

    @admin.action(description="Contract Removed")
    def contracts_lost(self, request, queryset):
        queryset.update(contract_status="REMOVED")

    @admin.action(description="Make Seamless")
    def change_contract_to_seamless(self, request, queryset):
        queryset.update(contract_type="SEAMLESS")

    @admin.action(description="Make Non-Seamless")
    def change_contract_to_non_seamless(self, request, queryset):
        queryset.update(contract_type="NON_SEAMLESS")

    @admin.action(description="Change Vat Rate to 5%")
    def change_vat_rate_to_5_percent(self, request, queryset):
        queryset.update(vat_rate="FIVE_PERCENT")

    change_vat_rate_to_5_percent.short_description = "Change VAT rate to 5 per cent"

    @admin.action(description="Change Vat Rate to 20%")
    def change_vat_rate_to_20_percent(self, request, queryset):
        queryset.update(vat_rate="TWENTY_PERCENT")

    change_vat_rate_to_20_percent.short_description = "Change VAT rate to 20 per cent"

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
            "contract_end_date",
            "eac",
            "commission_per_annum",
            "commission_per_unit",
        ]
        data = tablib.Dataset()
        data.headers = fields_to_export

        for obj in queryset:
            row = []
            for field in fields_to_export:
                if field == "contract_end_date":  # Check if the field is a date field
                    date_value = getattr(obj, field)
                    if date_value:  # Check if the date is not None
                        formatted_date = date_value.strftime("%d/%m/%Y")  # Format date to UK format
                        row.append(formatted_date)
                    else:
                        row.append("")  # Append empty string if date is None
                elif field == "commission_per_unit":  # Check if the field is commission_per_unit
                    commission_per_unit = getattr(obj, field)
                    if commission_per_unit in [0.01, 0.02, 0.03]:
                        # Keep the value unchanged
                        converted_value = commission_per_unit
                    else:
                        # Convert commission_per_unit to the desired format
                        converted_value = round(commission_per_unit * 100, 2)
                    row.append(converted_value)
                else:
                    row.append(getattr(obj, field))  # For non-date fields, just append the value
            data.append(row)

        response = HttpResponse(data.export("xlsx"), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment; filename="bulk_quote_template.xlsx"'
        return response

    bulk_quote_template.short_description = "Bulk Quote Template"

    def export_commissions_to_excel(self, request, queryset):
        # Check if the user has the 'can_export_commissions' permission
        if not request.user.has_perm("contracts.can_export_commissions"):
            # If the user does not have the permission, display a message and redirect
            messages.error(request, "You do not have permission to export commissions.")
            return HttpResponseRedirect(reverse("admin:index"))
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=commissions_by_utility.xlsx"

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Commissions by Client Contracts"

        columns = [
            "Client",
            "Contract Status",
            "Contract Type",
            "Originator",
            "Client Onboarded",
            "Utility",
            "Commission per Unit Rate",
            "Commission per Annum Rate",
            "Total EAC",
            "Number of Contracts",
            "Total Value per Contract",
        ]
        ws.append(columns)

        # Use the queryset directly which now reflects the user's selection
        selected_contracts = (
            queryset.values(
                "client__client",
                "contract_status",  # Assuming 'client' field is a ForeignKey to a Client model
                "contract_type",
                "client__originator",
                "client__client_onboarded",
                "utility__utility",  # Assuming 'utility' field is a ForeignKey to a Utility model
                "commission_per_unit",
                "commission_per_annum",
            )
            .annotate(
                total_eac=Sum("eac"),
                count=Count("id"),
                total_value_per_contract=ExpressionWrapper(
                    F("total_eac") * F("commission_per_unit"),
                    output_field=FloatField(),
                ),
            )
            .order_by("client__client", "utility__utility")
        )

        for contract in selected_contracts:
            ws.append(
                [
                    contract["client__client"],
                    contract["contract_status"],
                    contract["contract_type"],
                    contract["client__originator"],
                    contract["client__client_onboarded"],
                    contract["utility__utility"],
                    contract["commission_per_unit"],
                    contract["commission_per_annum"],
                    contract["total_eac"],
                    contract["count"],
                    contract["total_value_per_contract"],
                ]
            )

        wb.save(response)
        return response

    export_commissions_to_excel.short_description = "Export Commissions by to Excel"

    def link_to_clients(self, obj):
        link = reverse("admin:clients_client_change", args=[obj.client.id])
        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.client,
        )

    link_to_clients.short_description = "Clients"


admin.site.register(Contract, ContractAdmin)
