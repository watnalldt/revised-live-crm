from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, ListView

from contracts.models import Contract
from core.decorators import client_manager_required
from core.views import HTMLTitleMixin


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


@method_decorator([never_cache], name="dispatch")
class ContractListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Contract
    template_name = "contracts/all_contracts.html"
    context_object_name = "contracts"
    login_url = "/users/login/"

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()
