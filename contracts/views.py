from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from contracts.forms import ContractNotesForm
from contracts.models import Contract
from core.decorators import client_manager_required
from core.views import HTMLTitleMixin
from django.core.exceptions import PermissionDenied


@method_decorator([never_cache, client_manager_required], name="dispatch")
class ClientManagerContractDetail(LoginRequiredMixin, HTMLTitleMixin, DetailView):
    model = Contract
    template_name = "client_managers/contract_detail.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.business_name

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Contract.objects.filter(client_manager=self.request.user)
        else:
            return Contract.objects.none()


# class IsNotAdminMixin(UserPassesTestMixin):
#     def test_func(self):
#         return not self.request.user.is_staff
#
#
# class ContractCreateView(IsNotAdminMixin, CreateView):
#     model = Contract
#     form_class = ContractNotesForm
#     template_name = 'contracts/contract_form.html'
#     success_url = reverse_lazy('clients:client_contracts')
#
#     def get_form_class(self):
#         if self.request.user.is_staff:
#             return super().get_form_class()
#         return ContractNotesForm
#
#
# class ContractUpdateView(IsNotAdminMixin, UpdateView):
#     model = Contract
#     form_class = ContractNotesForm
#     template_name = 'contracts/contract_form.html'
#     success_url = reverse_lazy('contract_list')
#
#     def get_form_class(self):
#         if self.request.user.is_staff:
#             return super().get_form_class()
#         return ContractNotesForm


class ContractNotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractNotesForm
    template_name = "contracts/contract_form.html"
    login_url = "/users/login/"

    def get_queryset(self):
        # Get contracts where the account manager of the client is the current user
        return Contract.objects.filter(client__account_manager=self.request.user)

    def get_success_url(self):
        return reverse_lazy("clients:contract_detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        """Hook to ensure object is owned by request.user through the client relationship."""
        obj = super().get_object(queryset)
        if not obj.client.account_manager == self.request.user:
            raise PermissionDenied("You do not have permission to edit this contract.")
        return obj
