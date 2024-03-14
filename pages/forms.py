import datetime

from django import forms
from django_recaptcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=True)
    company = forms.CharField(max_length=50, required=False)

    message = forms.CharField(required=True, widget=forms.Textarea, label="Your Message Here:")
    captcha = ReCaptchaField()

    def clean_company(self):
        company = self.cleaned_data["company"]
        # Check if the company name is 'Google'
        if company.lower() == "google":
            raise forms.ValidationError("Google cannot be entered as a company name.")
        return company


class MeterReadingForm(forms.Form):
    CHOICES = [("gas", "Gas"), ("electricity", "Electricity")]

    name = forms.CharField(max_length=250, required=True)
    contact_email = forms.EmailField(max_length=50, required=True)
    address_of_meter = forms.CharField(max_length=250, required=True, label="Address of meter")
    current_supplier = forms.CharField(max_length=150, required=True, label="Current Supplier")
    mpan_mpr = forms.CharField(required=True, label="MPAN or MPR:")
    meter_serial_number = forms.CharField(required=True, label="Meter Serial Number")
    energy_type = forms.CharField(label="Utility Type", widget=forms.RadioSelect(choices=CHOICES))

    meter_reading_date = forms.CharField(
        widget=forms.widgets.DateTimeInput(format="%d/%m/%Y"),
        initial=datetime.date.today,
    )
    meter_reading = forms.CharField(
        required=True,
        label="Meter Read single or day/night. "
        "If day/night rate, separate the values with / e.g. 000000/000000. "
        "Please fill this in even if attaching a photo. ",
    )
    attachment = forms.FileField(
        required=False, label="Optionally upload a photo of your meter reading"
    )
