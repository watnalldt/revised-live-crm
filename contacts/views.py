from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView
from users.mixins import AccountManagerRequiredMixin
from .models import Contact, JobTitle
from django.urls import reverse_lazy
from .forms import ContactForm, JobTitleForm


class ContactListView(LoginRequiredMixin, AccountManagerRequiredMixin, ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


class ContactCreateView(LoginRequiredMixin, AccountManagerRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contacts")

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


class ContactUpdateView(LoginRequiredMixin, AccountManagerRequiredMixin, UpdateView):

    model = Contact
    template_name = "contacts/contact_form.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("contacts:contacts")

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()


class JobTitleCreateView(LoginRequiredMixin, AccountManagerRequiredMixin, CreateView):
    model = JobTitle
    form_class = JobTitleForm
    template_name = "contacts/job_title_form.html"
    success_url = reverse_lazy("contacts:create_contact")

    def test_func(self):
        return self.request.user.groups.filter(name="Account Managers").exists()
