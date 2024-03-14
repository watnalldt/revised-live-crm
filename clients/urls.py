from django.urls import path

from . import views

app_name = "clients"

urlpatterns = [
    path(
        "client_contracts/<int:pk>/",
        views.ClientDetailView.as_view(),
        name="client_contracts",
    ),
    path(
        "contract_detail/<int:pk>/",
        views.ContractDetailView.as_view(),
        name="contract_detail",
    ),
    path("all_clients/", views.ClientListView.as_view(), name="all_clients"),
    path(
        "all_client_contracts/<int:pk>/",
        views.AllClientsView.as_view(),
        name="all_client_contracts",
    ),
    path(
        "all_clients_contract_detail/<int:pk>/",
        views.AllContractsDetailView.as_view(),
        name="all_clients_contract_detail",
    ),
    # path("pdf/<pk>", views.contracts_render_pdf_view, name="contract_pdf_view"),
]
