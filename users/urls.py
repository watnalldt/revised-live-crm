from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # client manager registration
    path("register-user/", views.client_manager_registration, name="client_manager_registration"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path(
        "reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    # Dashboards
    path("my_account/", views.my_account, name="my_account"),
    # path(
    #     "account_managers_dashboard/",
    #     views.AccountManagerView.as_view(),
    #     name="account_managers_dashboard",
    # ),
    # path(
    #     "client_managers_dashboard/",
    #     views.ClientManagerDashBoard.as_view(),
    #     name="client_managers_dashboard",
    # ),
    # # Client List
    # path(
    #     "account_managers_client_list/",
    #     views.AccountManagerClientList.as_view(),
    #     name="client_list",
    # ),
    # path("search_results", views.SearchView.as_view(), name="search_results"),
    # path("out_of_contract/", views.OutOfContractListView.as_view(), name="out_of_contract"),
    # path(
    #     "expiring_contracts/", views.ExpiringContractsListView.as_view(), name="expiring_contracts"
    # ),
    # path(
    #     "directors_approval/", views.DirectorsApprovalListView.as_view(), name="directors_approval"
    # ),
    # path("expired_contracts/", views.ExpiredContractListView.as_view(), name="expired_contracts"),
    # path("lost_contracts/", views.LostContractsListView.as_view(), name="lost_contracts"),
    # path("locked_contracts/", views.LockedContractsListView.as_view(), name="locked_contracts"),
    # path("removed_contracts/", views.RemovedContractsListView.as_view(), name="removed_contracts"),
    # path(
    #     "under_objection/", views.UnderObjectionContractsListView.as_view(), name="under_objection"
    # ),
    # path("pricing_contracts/", views.ContractsPricingListView.as_view(), name="pricing_contracts"),
    # path("live_contracts/", views.LiveContractsListView.as_view(), name="live_contracts"),
    # path("new_contracts/", views.NewContractsListView.as_view(), name="new_contracts"),
]
