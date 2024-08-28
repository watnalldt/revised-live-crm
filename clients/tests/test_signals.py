import pytest
from django.utils import timezone
from ..models import Client
from ..signals import update_client_lost_date
from django.contrib.auth import get_user_model
from unittest.mock import patch

# Get the custom user model
User = get_user_model()


@pytest.mark.django_db
def test_update_client_lost_date():
    # Create an account manager using the custom user model
    account_manager = User.objects.create(
        password='manager',
        email='manager@example.com',
        # Add any other required fields for your custom user model
    )

    # Create a new client
    client = Client.objects.create(
        client="Test Client",
        is_lost=False,
        account_manager=account_manager
        # Add any other required fields for your Client model
    )

    print(f"Initial client_lost_date: {client.client_lost_date}")
    assert client.client_lost_date is None, "client_lost_date should be None for a new non-lost client"

    # Update client to lost status
    client.is_lost = True
    client.save()
    client.refresh_from_db()
    print(f"After setting is_lost=True: {client.client_lost_date}")
    assert client.client_lost_date == timezone.now().date(), ("client_lost_date should be set to today when client "
                                                              "becomes lost")

    # Update client back to not lost status
    client.is_lost = False
    client.save()
    client.refresh_from_db()
    print(f"After setting is_lost=False: {client.client_lost_date}")
    assert client.client_lost_date is None, "client_lost_date should be None when client is no longer lost"

    # Test creating a new client with is_lost=True
    new_client = Client.objects.create(
        client="New Lost Client",
        is_lost=True,
        account_manager=account_manager
        # Add any other required fields for your Client model
    )
    print(f"New lost client client_lost_date: {new_client.client_lost_date}")
    assert new_client.client_lost_date == timezone.now().date(), "client_lost_date should be set for a new lost client"

    # Test the DoesNotExist case
    with patch.object(Client.objects, 'get') as mock_get:
        mock_get.side_effect = Client.DoesNotExist

        # Create a client that will trigger the DoesNotExist exception
        non_existent_client = Client(
            id=999,  # Use an ID that doesn't exist in the database
            client="Non-existent Client",
            is_lost=True,
            account_manager=account_manager
        )

        # This should not raise an exception
        update_client_lost_date(sender=Client, instance=non_existent_client)

        # The client_lost_date should NOT be set in this case
        assert non_existent_client.client_lost_date is None, "client_lost_date should NOT be set when the object doesn't exist in the database"

