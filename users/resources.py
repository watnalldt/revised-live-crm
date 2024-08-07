from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth import get_user_model

from clients.models import Client
from contacts.models import Contact, JobTitle

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
