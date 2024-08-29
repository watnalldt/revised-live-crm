from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Contract
from users.models import AccountManager


class ClientFilter(AutocompleteFilter):
    title = "Client"
    field_name = "client"


class ClientManagerFilter(AutocompleteFilter):
    title = "Client Manager"
    field_name = "client_manager"


class SupplierFilter(AutocompleteFilter):
    title = "Supplier"  # display title
    field_name = "supplier"  # name of the foreign key field


class UtilityTypeFilter(AutocompleteFilter):
    title = "Utility Type"  # display title
    field_name = "utility"  # name of the foreign key field


class FutureSupplierFilter(AutocompleteFilter):
    title = "Future Supplier"  # display title
    field_name = "future_supplier"  # name of the foreign key field


# Custom Filters ----------------------------------------------------------------
class AccountManagerFilter(admin.SimpleListFilter):
    title = "Account Manager"
    parameter_name = "account_manager"

    def lookups(self, request, model_admin):
        # Return a list of tuples (value, verbose_name) for the filter options
        account_managers = AccountManager.objects.all()
        return [(manager.email, manager.email) for manager in account_managers]

    def queryset(self, request, queryset):
        # Filter the queryset based on the selected account manager's email
        if self.value():
            return queryset.filter(client__account_manager__email=self.value())
        return queryset


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
