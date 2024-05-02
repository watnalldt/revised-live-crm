from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from clients.models import Client
from utilities.models import Supplier

from .models import Objection


class ObjectionResource(resources.ModelResource):
    client = fields.Field(
        column_name="client",
        attribute="client",
        widget=ForeignKeyWidget(Client, "client"),
    )

    new_supplier = fields.Field(
        column_name="new_supplier",
        attribute="new_supplier",
        widget=ForeignKeyWidget(Supplier, "supplier"),
    )

    objecting_supplier = fields.Field(
        column_name="objecting_supplier",
        attribute="objecting_supplier",
        widget=ForeignKeyWidget(Supplier, "supplier"),
    )

    class Meta:
        model = Objection
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ("id",)


class ClientFilter(AutocompleteFilter):
    title = "Client"  # display title
    field_name = "client"  # name of the foreign key field


class ObjectingSupplierFilter(AutocompleteFilter):
    title = "Objecting Supplier"  # display title
    field_name = "objecting_supplier"  # name of the foreign key field


class NewSupplierFilter(AutocompleteFilter):
    title = "New Supplier"  # display title
    field_name = "new_supplier"  # name of the foreign key field


class ObjectionAdmin(ImportExportModelAdmin):
    show_full_result_count = False
    resource_class = ObjectionResource
    list_select_related = ("client",)
    list_display = (
        "client",
        "objection_status",
        "mpan_mpr",
        "objecting_supplier",
        "new_supplier",
        "registration_date",
        "objection_date",
        "deadline_date",
        "eac",
    )
    list_filter = (
        ClientFilter,
        "objection_status",
        ObjectingSupplierFilter,
        NewSupplierFilter,
        "is_directors_approval",
    )
    autocomplete_fields = [
        "client",
        "objecting_supplier",
        "new_supplier",
    ]
    search_fields = (
        "client__client",
        "mpan_mpr",
        "objecting_supplier__supplier",
    )
    list_per_page = 25
    # Change Objection Status Management Commands
    actions = ["objection_status_pending", "objection_status_resolved"]

    @admin.action(description="Objection Status Pending")
    def objection_status_pending(self, request, queryset):
        queryset.update(objection_status="PENDING")

    @admin.action(description="Objection Status Resolved")
    def objection_status_resolved(self, request, queryset):
        queryset.update(objection_status="RESOLVED")


admin.site.register(Objection, ObjectionAdmin)
