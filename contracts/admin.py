from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .models import Contract
from .filters import (
    ClientFilter,
    SupplierFilter,
    UtilityTypeFilter,
    MultiStatusFilter,
    AccountManagerFilter,
)
from rangefilter.filters import DateRangeFilter
from .admin_actions import (
    directors_approval_not_required,
    directors_approval_required,
    seamless_contract_updated,
    seamless_contract_not_updated,
    out_of_contract,
    make_contract_live,
    make_contract_pricing,
    make_contract_objection,
    make_contract_locked,
    contracts_removed,
    contracts_lost,
    bulk_quote_template,
    export_commissions_to_excel,
    export_expired_contracts,
    export_corona_live_duplicates,
    export_sse_live_duplicates,
    export_to_excel_and_pdfs,
)
from .custom_search import CustomSearchAdmin
from .resources import ContractResource


class ContractAdmin(ImportExportModelAdmin, ExportActionMixin, CustomSearchAdmin):
    list_per_page = 20
    show_full_result_count = False
    resource_class = ContractResource
    ordering = ("contract_end_date",)
    readonly_fields = ("commission_per_annum", "commission_per_unit")
    list_select_related = ("client", "client_manager", "supplier", "utility")
    fieldsets = (
        (
            "Site Information",
            {
                "description": "Enter the site details",
                "fields": (
                    ("client", "client_group", "business_name", "client_manager"),
                    "site_address",
                    "seed_stock",
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
    list_display = (
        "id",
        "contract_status",
        "business_name",
        "contract_type",
        "seamless_updated",
        "client",
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
    list_filter = [
        "contract_type",
        "seamless_updated",
        AccountManagerFilter,
        ClientFilter,
        "client_group",
        SupplierFilter,
        UtilityTypeFilter,
        MultiStatusFilter,
        "seamless_status",
        "seed_stock",
        "is_ooc",
        "is_directors_approval",
        ("contract_end_date", DateRangeFilter),
        ("contract_start_date", DateRangeFilter),
        "vat_rate",
        "vat_declaration_sent",
        "meter_status",
    ]
    autocomplete_fields = [
        "client",
        "client_manager",
        "supplier",
    ]

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
        directors_approval_not_required,
        directors_approval_required,
        seamless_contract_updated,
        seamless_contract_not_updated,
        out_of_contract,
        make_contract_live,
        make_contract_pricing,
        make_contract_objection,
        make_contract_locked,
        contracts_lost,
        contracts_removed,
        bulk_quote_template,
        export_commissions_to_excel,
        export_expired_contracts,
        export_corona_live_duplicates,
        export_sse_live_duplicates,
        export_to_excel_and_pdfs,
    ]


admin.site.register(Contract, ContractAdmin)
