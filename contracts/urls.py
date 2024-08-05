from django.urls import path

from . import views


app_name = "contracts"

urlpatterns = [
    path(
        "client_contract_detail/<int:pk>/",
        views.ClientManagerContractDetail.as_view(),
        name="client_contract_detail",
    ),
    # path('contracts/<int:pk>/update_notes/', update_contract_notes, name='update_contract_notes'),
    path(
        "contracts/notes/<int:pk>/edit/",
        views.ContractNotesUpdateView.as_view(),
        name="contract_notes_update",
    ),
    path("contract-status-count/", views.contract_status_count, name="contract_status_count"),
    path("contract/<int:pk>/add/", views.ContractCreateView.as_view(), name="contract_note_add"),
    path("contract/<int:pk>/edit/", views.ContractUpdateView.as_view(), name="contract_note_edit"),
]
