from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic import View
from django.contrib.auth import get_user_model

from ..mixins import AccountManagerRequiredMixin  # Adjust the import path as necessary

User = get_user_model()


class MockView(AccountManagerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # This view simply returns HTTP 200 if the user passes the test, otherwise forbidden
        return HttpResponse() if self.test_func() else HttpResponseForbidden()


class AccountManagerRequiredMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email="user@test.com", password="top_secret")
        self.account_manager_group = Group.objects.create(name="Account Managers")

    def test_user_is_account_manager(self):
        # Add the user to the "Account Managers" group
        self.user.groups.add(self.account_manager_group)
        self.user.save()

        # Create a request object
        request = self.factory.get("/fake-path")
        request.user = self.user

        # Instantiate the view with the request object
        view = MockView.as_view()
        response = view(request)

        # Check that the view returns HTTP 200
        self.assertEqual(response.status_code, 200)
