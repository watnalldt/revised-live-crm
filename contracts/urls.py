from django.urls import path

from . import views

app_name = "contracts"

urlpatterns = [
    path(
        "client_contract_detail/<int:pk>/",
        views.ClientManagerContractDetail.as_view(),
        name="client_contract_detail",
    ),
    path("contracts_chart", views.contracts_chart, name="contracts_chart"),
    path("top_consumption", views.top_consumption, name="top_consumption"),
    path(
        "top_electricity_commissions",
        views.top_electricity_commissions,
        name="top_electricity_commissions",
    ),
    path("top_gas_commissions", views.top_gas_commissions, name="top_gas_commissions"),
    path("contract_filter", views.FilterAndExportView.as_view(), name="contracts_filter"),
]
