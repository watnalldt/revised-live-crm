from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, ListView

from contracts.models import Contract
from core.decorators import account_manager_required
from core.views import HTMLTitleMixin

from .forms import MeterForm, MultipleMeterForm
from .models import Client


@method_decorator([account_manager_required, never_cache], name="dispatch")
class ClientDetailView(LoginRequiredMixin, HTMLTitleMixin, DetailView):
    """Details all contracts for that client by account manager"""

    model = Client
    template_name = "clients/contracts/client_detail.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.client

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(account_manager=self.request.user)
        else:
            return Client.objects.none()


@method_decorator([never_cache, account_manager_required], name="dispatch")
class ContractDetailView(LoginRequiredMixin, HTMLTitleMixin, DetailView):
    """Details individual contracts for that client by client manager"""

    model = Contract

    template_name = "clients/contracts/contract_detail.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.business_name

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Contract.objects.filter(client__account_manager=self.request.user)
        else:
            return Contract.objects.none()


# return all clients and associated contracts
class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    context_object_name = "all_clients"
    template_name = "clients/contracts/all_contracts/all_clients.html"
    login_url = "/users/login/"

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


class AllClientsView(LoginRequiredMixin, UserPassesTestMixin, HTMLTitleMixin, DetailView):
    queryset = Client.objects.all()
    template_name = "clients/contracts/all_contracts/all_client_contracts.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.client

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


class AllContractsDetailView(LoginRequiredMixin, UserPassesTestMixin, HTMLTitleMixin, DetailView):
    model = Contract
    template_name = "clients/contracts/all_contracts/all_contracts_detail.html"
    login_url = "/users/login/"

    def get_html_title(self):
        return self.object.business_name

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


def get_contract_and_init_form(request, pk, form_class):
    """
    Utility function to get contract and initialize form with initial data.
    """
    contract = get_object_or_404(Contract, pk=pk, client_manager=request.user.id)
    form = form_class(
        initial={
            "from_email": request.user.email,
            "client_name": contract.client,
            "site_address": contract.site_address,
            "mpan_mpr": contract.mpan_mpr,
            "meter_serial_number": contract.meter_serial_number,
            "utility_type": contract.utility,
            "supplier": contract.supplier,
        }
    )
    return contract, form


def send_meter_email(request, subject, template, data, attachment=None):
    """
    Utility function to prepare and send the meter reading email.
    """
    message = get_template(template).render(data)
    recipient_list = (
        ["meterreads@energyportfolio.co.uk", data["supplier_meter_email"]]
        if data["supplier_meter_email"]
        else ["meterreads@energyportfolio.co.uk"]
    )
    try:
        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        if attachment:
            mail.attach(attachment.name, attachment.read(), attachment.content_type)
        mail.content_subtype = "html"
        mail.send()
    except BadHeaderError:
        return HttpResponse("Invalid header found.")


def meter_reading_base(request, pk, form_class, template, email_template):
    """
    Base view function for handling meter reading submissions.
    """
    contract, form = get_contract_and_init_form(request, pk, form_class)

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data.update(
                {
                    "supplier_meter_email": contract.supplier.meter_email,
                    "subject": "Meter Reading" if form_class == MeterForm else "Meter Readings",
                }
            )
            attachment = request.FILES.get("attachment") if "attachment" in request.FILES else None
            send_meter_email(request, data["subject"], email_template, data, attachment)
            messages.success(request, "Your meter reading has been received.")
            return redirect("users:my_account")

    return render(request, template, {"form": form, "contract": contract})


# Updated view functions
def meter_reading(request, pk):
    return meter_reading_base(
        request,
        pk,
        MeterForm,
        "client_managers/meter_reading.html",
        "clients/contracts/meter_reading_submission.html",
    )


def multiple_meter_reading(request, pk):
    return meter_reading_base(
        request,
        pk,
        MultipleMeterForm,
        "client_managers/multiple_meter_reading.html",
        "clients/contracts/multiple_meter_reading_submission.html",
    )
