from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template, render_to_string
from django.views.generic import TemplateView

from core.views import HTMLTitleMixin

from .forms import ContactForm, MeterReadingForm


class HomePageView(HTMLTitleMixin, TemplateView):
    template_name = "pages/index.html"
    html_title = "Effectively Managing Energy Solutions"


class MarketUpdateView(HTMLTitleMixin, TemplateView):
    template_name = "pages/market_update.html"
    html_title = "Energy Portfolio Market Update"


class SeamlessUtilitiesView(HTMLTitleMixin, TemplateView):
    template_name = "pages/seamless_utilities.html"
    html_title = "Energy Portfolio Seamless Utilities"


class PartnersView(HTMLTitleMixin, TemplateView):
    template_name = "pages/our_partners.html"
    html_title = "Energy Portfolio Our Partners"


class OurServicesView(HTMLTitleMixin, TemplateView):
    template_name = "pages/our_services.html"
    html_title = "Energy Portfolio Our Services"


class ComplaintsPolicyView(HTMLTitleMixin, TemplateView):
    template_name = "pages/complaints_policy.html"
    html_title = "EP Complaints Policy"


class PrivacyPolicyView(HTMLTitleMixin, TemplateView):
    template_name = "pages/privacy_policy.html"
    html_title = "EP Privacy Policy"


def meter_reading_submission(request):
    template = "pages/meter_submission.html"
    if request.method == "POST":
        meter_form = MeterReadingForm(request.POST, request.FILES)
        if meter_form.is_valid():
            subject = "Meter Reading"
            data = {
                "name": meter_form.cleaned_data["name"],
                "contact_email": meter_form.cleaned_data["contact_email"],
                "address_of_meter": meter_form.cleaned_data["address_of_meter"],
                "current_supplier": meter_form.cleaned_data["current_supplier"],
                "mpan_mpr": meter_form.cleaned_data["mpan_mpr"],
                "meter_serial_number": meter_form.cleaned_data["meter_serial_number"],
                "energy_type": meter_form.cleaned_data["energy_type"],
                "meter_reading_date": meter_form.cleaned_data["meter_reading_date"],
                "meter_reading": meter_form.cleaned_data["meter_reading"],
            }
            message = get_template("pages/meter_reading_submission.html").render(data)
            try:
                mail = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ["meterreads@energyportfolio.co.uk"],
                )
                if "attachment" in request.FILES:
                    attachment = request.FILES.get("attachment")
                    mail.attach(attachment.name, attachment.read(), attachment.content_type)

                mail.content_subtype = "html"
                mail.send()

            except BadHeaderError:
                return HttpResponse("Invalid header found.")
        messages.success(request, "Your meter reading has been received.")
        return redirect("pages:home")
    form = MeterReadingForm()
    return render(request, template, {"meter_form": form})


def contact_us(request):
    template = "pages/contact.html"
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            company = form.cleaned_data["company"]
            message = form.cleaned_data["message"]

            html = render_to_string(
                "pages/contact_template.html",
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "company": company,
                    "message": message,
                },
            )

            send_mail(
                "New Contact Form Submission",
                "This is the message",
                from_email="david@energyportfolio.co.uk",
                recipient_list=[
                    "david@energyportfolio.co.uk",
                ],
                html_message=html,
            )
            messages.success(request, "We will be in touch with you shortly.")
            return redirect("pages:home")
    else:
        form = ContactForm()

    return render(request, template, {"form": form})
