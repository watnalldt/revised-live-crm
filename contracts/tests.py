from django.test import TestCase
from contracts.models import Contract, ContractsManager
from clients.models import Client
from utilities.models import Supplier, Utility
from users.models import AccountManager


class ContractsManagerTestCase(TestCase):
    def setUp(self):
        # Set up related objects
        self.account_manager = AccountManager.objects.create(email="Manager1@example.com")
        self.client = Client.objects.create(client="Client1", account_manager=self.account_manager)
        self.supplier = Supplier.objects.create(supplier="Supplier1")
        self.utility = Utility.objects.create(utility="Utility1")

        # Create a contract linking to all the above
        self.contract = Contract.objects.create(
            client=self.client,
            supplier=self.supplier,
            utility=self.utility,
            mpan_mpr="1234567890123",
            business_name="The White House",
        )

    def test_get_queryset_includes_related_objects(self):
        # Use the ContractsManager to get the queryset
        manager = ContractsManager()
        manager.model = Contract  # Associate model with manager for testing
        queryset = manager.get_queryset().select_related(
            "client", "client_manager", "supplier", "utility"
        )  # Ensure all related objects are fetched together

        # Fetch a contract from the queryset
        contract_with_related = queryset.get(id=self.contract.id)

        # Access related objects and ensure they do not perform new queries
        with self.assertNumQueries(0):
            print(contract_with_related.client.client)
            print(contract_with_related.supplier.supplier)
            print(contract_with_related.utility.utility)
            print(contract_with_related.mpan_mpr)
            print(contract_with_related.business_name)

            # Assert that the objects are correctly related
        self.assertEqual(contract_with_related.client, self.client)
        self.assertEqual(contract_with_related.supplier, self.supplier)
        self.assertEqual(contract_with_related.utility, self.utility)
        self.assertEqual(contract_with_related.mpan_mpr, "1234567890123")
        self.assertEqual(contract_with_related.business_name, "The White House")
