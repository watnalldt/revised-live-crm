from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from core.decorators import admin_changelist_link

from .models import Supplier, Utility


class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        skip_unchanged = True
        report_skipped = True
        # fields = ["supplier"]
        import_id_fields = ["supplier"]


class SupplierAdmin(ImportExportModelAdmin):
    resource_class = SupplierResource
    list_display = ("supplier", "meter_email", "suppliers_link")
    list_filter = ("supplier",)
    ordering = ("supplier",)
    search_fields = ("supplier",)

    @admin_changelist_link(
        "contract_suppliers", _("All Contracts"), query_string=lambda c: f"supplier_id={c.pk}"
    )
    def suppliers_link(self, contract_suppliers):
        return _("All Contracts")


admin.site.register(Supplier, SupplierAdmin)


class UtilityResource(resources.ModelResource):
    class Meta:
        model = Utility
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ["utility"]


class UtilityAdmin(admin.ModelAdmin):
    list_display = ("utility", "utilities_link")
    search_fields = ("utility",)
    ordering = ("utility",)

    @admin_changelist_link(
        "contract_utilities", _("All Contracts"), query_string=lambda c: f"utility_id={c.pk}"
    )
    def utilities_link(self, contract_utilities):
        return _("All Contracts")


admin.site.register(Utility, UtilityAdmin)
