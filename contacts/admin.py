from django.contrib import admin
from .models import JobTitle, Contact
from clients.models import Client
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class JobTitleAdmin(admin.ModelAdmin):
    inlines = (ContactInline,)


admin.site.register(JobTitle, JobTitleAdmin)


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
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "client" "job_title",
        ]
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


admin.site.register(Contact, ContactAdmin)
