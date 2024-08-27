from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model
from contracts.models import Contract
from clients.models import Client
from contacts.models import Contact, JobTitle
from utilities.models import Supplier, Utility

User = get_user_model()


class ClientResource(resources.ModelResource):
    account_manager = fields.Field(
        column_name="account_manager",
        attribute="account_manager",
        widget=ForeignKeyWidget(User, "email"),
    )

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
