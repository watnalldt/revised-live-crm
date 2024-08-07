from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from .models import Contract
from clients.models import Client
from utilities.models import Supplier, Utility
from django.contrib.auth import get_user_model

User = get_user_model()


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
        export_order = (
            "id",
            "contract_type",
            "seamless_updated",
            "contract_status",
            "client",
            "client_group",
            "client_manager",
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
