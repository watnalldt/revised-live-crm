# from django.contrib.auth.models import Group
# from django.test import TestCase, Client as TestClient
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from ..models import Contact
# from clients.models import Client
#
# User = get_user_model()
#
#
# class TestContactListView(TestCase):
#     def setUp(self):
#         # Create a user and authenticate
#         self.account_manager = User.objects.create_user(
#             email="manager@example.com", password="test"
#         )
#         self.test_client = TestClient()
#         self.test_client.login(email="manager@example.com", password="test")
#
#         # Create a group and add the account manager to it
#         self.group = Group.objects.create(name="Account Managers")
#         self.account_manager.groups.add(self.group)
#
#         # Create a client and assign the account manager
#         self.client_model = Client.objects.create(
#             name="Client A", account_manager=self.account_manager
#         )
#
#         # Create some contacts
#         Contact.objects.create(name="Alice", client=self.client_model, email="alice@example.com")
#
#     def test_list_view_with_permissions(self):
#         # Define the user agent
#         desktop_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#
#         # Pass the user agent in the headers
#         response = self.test_client.get(
#             reverse("contacts:contact_list"),
#             HTTP_USER_AGENT=desktop_user_agent
#         )
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "contacts/contact_list.html")
#         self.assertTrue("contacts" in response.context)
#         self.assertTrue(
#             all(
#                 contact.client.account_manager == self.account_manager
#                 for contact in response.context["contacts"]
#             )
#         )
