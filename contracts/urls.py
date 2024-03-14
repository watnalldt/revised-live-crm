from django.urls import path

from . import views

app_name = "contracts"

urlpatterns = [
    path(
        "client_contract_detail/<int:pk>/",
        views.ClientManagerContractDetail.as_view(),
        name="client_contract_detail",
    ),
    path("all_contracts", views.ContractListView.as_view(), name="all_contracts"),
]
