from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import ListView, TemplateView, View


from clients.models import Client
from contracts.models import Contract
from core.decorators import account_manager_required, client_manager_required
from core.views import HTMLTitleMixin

from .forms import RegistrationForm
from .mixins import AccountManagerRequiredMixin
from .utils import detect_user, send_verification_email

User = get_user_model()


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    """
    Display login form and handle login logic.

    If user is already authenticated, redirect to 'users:my_account'.
    If form is submitted via POST method, attempt authentication.
    If authentication is successful, redirect to 'users:my_account'.
    If authentication fails, display error message.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered login page or redirection.
    """
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("users:my_account")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd["username"], password=cd["password"])

            if user is not None:
                auth.login(request, user)
                messages.success(request, " You are logged in..")
                return redirect("users:my_account")
            else:
                messages.error(request, "Invalid login credentials..")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "You have successfully logged out.")
    return redirect("users:login")


@login_required(login_url="users:login")
def my_account(request):
    """
    View function for handling requests to the 'my_account' page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the appropriate URL based on their user type.
    """
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


def client_manager_registration(request):
    """
    Handles client manager registration.

    This view function handles both the registration form submission and rendering
    the registration page. If the request method is POST, it processes the form data,
    creates a new user, sends an activation email, and redirects to the registration page.
    If the request method is GET, it renders the registration form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing either the registration form or a
        redirection to the registration page.
    """
    if request.method == "POST":
        # store the data and create the user
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password
            )
            user.role = User.Roles.CLIENT_MANAGER
            user.is_active = False  # Disable account until email confirmation
            user.save()
            mail_subject = "Please activate your account"
            email_template = "users/registration/emails/account_verification_email.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Please check your emails to activate your account")
            return redirect("users:client_manager_registration")

    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "users/registration/register_client_manager.html", context)


def activate(request, uidb64, token):
    """
    Activates a user's account based on the provided UID and token.

    This view function activates a user's account if the UID and token are valid.
    It also notifies certain administrators when the account is activated.

    Args:
        request (HttpRequest): The HTTP request object.
        uidb64 (str): The base64-encoded user ID.
        token (str): The activation token.

    Returns:
        HttpResponse: The HTTP response indicating success or failure.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Notify certain admins when the account is activated
        recipients = [
            "recipient1@example.com",
            "recipient2@example.com",
        ]  # Add the email addresses of the recipients you want to notify
        notification_subject = "Account Activated"
        notification_message = f"The account with email {user.email} has been activated."

        send_mail(
            notification_subject, notification_message, "support@energyportfolio.co.uk", recipients
        )
        messages.success(request, "Your account is activated")
        return redirect("users:my_account")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("users:my_account")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST["email"]

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = "Reset Your Password"
            email_template = "users/emails/reset_password_email.html"
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, "Password reset link has been sent to your email address.")
            return redirect("users:login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("users:forgot_password")
    return render(request, "users/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.info(request, "Please reset your password")
        return redirect("users:reset_password")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("users:my_account")


def reset_password(request):
    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("users:login")
        else:
            messages.error(request, "Password do not match!")
            return redirect("users:reset_password")

    return render(request, "users/reset_password.html")


@method_decorator([never_cache, account_manager_required], name="dispatch")
class AccountManagerView(LoginRequiredMixin, HTMLTitleMixin, TemplateView):
    # Returns the Account Manager's Dashboard on login.
    model = Client
    template_name = "account_managers/account_managers_dashboard.html"
    html_title = "My Dashboard"


@method_decorator([never_cache, account_manager_required], name="dispatch")
class AccountManagerClientList(LoginRequiredMixin, HTMLTitleMixin, ListView):
    # Lists out all their client's with a link to their respective contracts
    model = Client
    template_name = "account_managers/client_list.html"
    html_title = "Client List"
    login_url = "/users/login/"

    def get_queryset(self):
        return Client.objects.filter(account_manager=self.request.user)


@method_decorator([never_cache, client_manager_required], name="dispatch")
class ClientManagerDashBoard(LoginRequiredMixin, HTMLTitleMixin, ListView):
    """Returns the Client Manager's Dashboard on login.
    Lists out all the client's contracts with a link to the detail"""

    model = Contract
    template_name = "client_managers/client_managers_dashboard.html"
    html_title = "Contracts List"
    login_url = "/users/login/"

    def get_queryset(self):
        return Contract.objects.filter(client_manager=self.request.user)


class SearchView(LoginRequiredMixin, AccountManagerRequiredMixin, View):
    @classmethod
    @method_decorator(never_cache)
    @method_decorator(account_manager_required)
    def get(cls, request, *args, **kwargs):
        query = request.GET.get("q", "")  # Get the query from the request
        contracts = Contract.objects.filter(
            Q(mpan_mpr__iexact=query)
            | Q(meter_serial_number__iexact=query)
            | Q(business_name__icontains=query)
            | Q(site_address__icontains=query)
            | Q(client__client__icontains=query)
        )  # Search

        # # Pagination
        # paginator = Paginator(contracts, 10)  # Show 10 clients per page
        # page_number = request.GET.get("page")
        # page_obj = paginator.get_page(page_number)

        return render(
            request,
            "account_managers/search_results.html",
            {"contracts": contracts, "query": query},
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class OutOfContractListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/out_of_contract_list.html"
    context_object_name = "ooc_contracts"

    def get_queryset(self):
        # Filter contracts that are out of contract
        return Contract.objects.filter(is_ooc="YES").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class DirectorsApprovalListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/directors_approval_list.html"
    context_object_name = "da_contracts"

    def get_queryset(self):
        # Filter contracts that require directors approval
        return Contract.objects.filter(is_directors_approval="YES").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class ExpiredContractListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/expired_contracts_list.html"
    context_object_name = "expired_contracts"

    def get_queryset(self):
        # Parse the end date to compare with 01/01/2024
        end_date = datetime.strptime("01/01/2024", "%d/%m/%Y")
        # Filter contracts where the contract end date is before January 1, 2024
        return (
            super()
            .get_queryset()
            .filter(contract_end_date__lt=end_date)
            .filter(client__account_manager=self.request.user)
        )


class ExpiringContractsListView(LoginRequiredMixin, AccountManagerRequiredMixin, View):
    @classmethod
    @method_decorator(never_cache, name="dispatch")
    @method_decorator(account_manager_required, name="dispatch")
    def get(cls, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%d/%m/%Y").date()
            end_date = datetime.strptime(end_date, "%d/%m/%Y").date()
            client__account_manager = (
                request.user
            )  # Assuming account manager is a foreign key in the User model
            contracts = Contract.objects.filter(
                contract_end_date__range=[start_date, end_date],
                client__account_manager=client__account_manager,
            )

        else:
            contracts = Contract.objects.filter(client__account_manager=request.user)

        return render(
            request, "account_managers/expiring_contract_list.html", {"contracts": contracts}
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class LostContractsListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/lost_contracts_list.html"
    context_object_name = "lost_contracts"

    def get_queryset(self):
        # Filter contracts that require directors approval
        return Contract.objects.filter(contract_status="LOST").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class LockedContractsListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/locked_contracts_list.html"
    context_object_name = "locked_contracts"

    def get_queryset(self):
        # Filter contracts that are locked
        return Contract.objects.filter(contract_status="LOCKED").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class RemovedContractsListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/removed_contracts_list.html"
    context_object_name = "removed_contracts"

    def get_queryset(self):
        # Filter contracts that designated removed
        return Contract.objects.filter(contract_status="REMOVED").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class UnderObjectionContractsListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/objected_contracts_list.html"
    context_object_name = "objected_contracts"

    def get_queryset(self):
        # Filter contracts that designated removed
        return Contract.objects.filter(contract_status="OBJECTION").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class ContractsPricingListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/pricing_contracts_list.html"
    context_object_name = "pricing_contracts"

    def get_queryset(self):
        # Filter contracts that designated removed
        return Contract.objects.filter(contract_status="PRICING").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class LiveContractsListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/live_contracts_list.html"
    context_object_name = "live_contracts"

    def get_queryset(self):
        # Filter contracts that designated removed
        return Contract.objects.filter(contract_status="LIVE").filter(
            client__account_manager=self.request.user
        )


@method_decorator(never_cache, name="dispatch")
@method_decorator(account_manager_required, name="dispatch")
class NewContractsListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contract
    template_name = "account_managers/new_contracts_list.html"
    context_object_name = "new_contracts"

    def get_queryset(self):
        # Filter contracts that designated removed
        return Contract.objects.filter(contract_status="NEW").filter(
            client__account_manager=self.request.user
        )
