from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from clients.models import Client
from .models import Contact, JobTitle
from django_select2.forms import ModelSelect2Widget


class ContactForm(ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        widget=ModelSelect2Widget(model=Client, search_fields=["client__icontains"]),
    )

    class Meta:
        model = Contact
        fields = ("client", "name", "email", "job_title", "phone_number")

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        # Example to dynamically set queryset based on user if needed:
        # if 'user' in kwargs:
        #     user = kwargs.pop('user')
        #     self.fields['client'].queryset = Client.objects.filter(user=user)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            raise ValidationError("Invalid email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        job_title = cleaned_data.get("job_title")
        if self._contact_with_different_job_title_exists(name, job_title):
            self.add_error("name", "This contact already has an assigned job title.")
        return cleaned_data

    def _contact_with_different_job_title_exists(self, name, job_title):
        query = Contact.objects.filter(name=name).exclude(job_title=job_title)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
        return query.exists()


class JobTitleForm(ModelForm):

    class Meta:
        model = JobTitle
        fields = [
            "title",
        ]
