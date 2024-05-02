from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, View
from django.db.models import Count
from django.shortcuts import render
from contracts.models import Contract
from core.decorators import client_manager_required
from core.views import HTMLTitleMixin
from django.http import JsonResponse, HttpRequest
from typing import Dict, List
from django.http import HttpResponse

import xlsxwriter
from io import BytesIO


@method_decorator([never_cache, client_manager_required], name="dispatch")
class ClientManagerContractDetail(LoginRequiredMixin, HTMLTitleMixin, DetailView):
    model = Contract
    template_name = "client_managers/contract_detail.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.business_name

    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         client__client_manager__client_manager=self.request.user
    #     )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Contract.objects.filter(client_manager=self.request.user)
        else:
            return Contract.objects.none()


# @method_decorator([never_cache], name="dispatch")
# class ContractListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model = Contract
#     template_name = "contracts/all_contracts.html"
#     context_object_name = "contracts"
#     login_url = "/users/login/"
#
#     def test_func(self):
#         return self.request.user.groups.filter(name="Account Managers").exists()


def contracts_chart(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # This part handles the AJAX request for the chart data
        labels = []
        data = []

        contract_data = Contract.objects.values("contract_status").annotate(
            total=Count("contract_status")
        )

        # Populate labels and data lists
        for entry in contract_data:
            labels.append(entry["contract_status"])
            data.append(entry["total"])
        return JsonResponse(
            data={
                "labels": labels,
                "data": data,
            }
        )

    # Pass labels and data separately to the context
    return render(request, "contracts/charts/contract_status.html")


def top_consumption(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # This part handles the AJAX request for the chart data
        # Initialize lists to hold chart labels and data

        labels = []
        data = []
        queryset = Contract.consumption.top_clients_by_eac()

        for entry in queryset:
            labels.append(entry["client__client"])
            data.append(entry["total_eac"])

        return JsonResponse(
            data={
                "labels": labels,
                "data": data,
            }
        )
    return render(request, "contracts/charts/top_consumption.html")


def get_ajax_data(queryset) -> Dict[str, List]:
    """
    Helper function to process the queryset and return the data suitable for chart representation.

    :param queryset: Django queryset containing top clients data.
    :return: Dictionary with labels and corresponding data.
    """
    labels = [entry["client__client"] for entry in queryset]
    data = [entry["total_value"] for entry in queryset]
    return {"labels": labels, "data": data}


def top_electricity_commissions(request: HttpRequest):
    """
    View to display the top electricity commissions either as a chart for AJAX requests
    or render a HTML page for standard requests.

    :param request: HttpRequest object.
    :return: JsonResponse if AJAX request, otherwise rendered HTML page.
    """
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Fetch the top clients by total value using the custom manager method
        queryset = Contract.electricity_commissions.top_clients_by_total_value()[:30]
        ajax_data = get_ajax_data(queryset)

        # Return a JsonResponse with labels and data formatted for charting
        return JsonResponse(ajax_data)

    return render(request, "contracts/charts/top_electricity_commissions.html")


def top_gas_commissions(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # This part handles the AJAX request for the chart data
        labels = []
        data = []
        queryset = Contract.gas_commissions.top_clients_by_total_value()[
            :30
        ]  # Limit to top 30 clients

        for entry in queryset:
            labels.append(entry["client__client"])
            data.append(entry["total_value"])

        return JsonResponse(
            {
                "labels": labels,
                "data": data,
            }
        )

    # This part renders the initial HTML template
    return render(request, "contracts/charts/top_gas_commissions.html")


class FilterAndExportView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve filters from request parameters
        utility_filter = request.GET.get("utility")
        client_filter = request.GET.get("client")
        contract_type_filter = request.GET.get("contract_type")
        status_filter = request.GET.get("status")

        # Start building the queryset
        contracts = Contract.objects.all()

        # Apply filters if they exist
        if utility_filter:
            contracts = contracts.filter(utility__utility=utility_filter)
        if client_filter:
            contracts = contracts.filter(client__client=client_filter)
        if contract_type_filter:
            contracts = contracts.filter(contract_type=contract_type_filter)
        if status_filter:
            contracts = contracts.filter(contract_status=status_filter)

        # Create an output stream
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Contracts")

        # Define headers for Excel file
        headers = [
            "Client",
            "Utility",
            "Contract Type",
            "Status",
            "Start Date",
            "End Date",
            "Value",
        ]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Populate the Excel file with filtered data
        for row_num, contract in enumerate(contracts, start=1):
            row = [
                contract.client.client,
                contract.utility.utility,
                contract.get_contract_type_display(),
                contract.get_contract_status_display(),
                contract.contract_start_date,
                contract.contract_end_date,
                contract.contract_value,
            ]
            for col_num, cell_value in enumerate(row):
                worksheet.write(row_num, col_num, cell_value)

        # Close the workbook after writing all the data
        workbook.close()

        # Rewind the buffer
        output.seek(0)

        # Set up the HTTP response
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="filtered_contracts.xlsx"'

        return response
