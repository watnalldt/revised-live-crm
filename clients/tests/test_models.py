import pytest
from django.urls import reverse
from mixer.backend.django import mixer  # or any other library for creating test data
from clients.models import Client

pytestmark = pytest.mark.django_db


def test_client_creation():
    assert isinstance(mixer.blend(Client), Client)


def test_client_absolute_url():
    created_client = mixer.blend(Client)  # Use created_client where reference is needed
    assert created_client.get_absolute_url() == reverse(
        "clients:client_contracts", args=[str(created_client.pk)]
    )


def test_client_str():
    client_name = "Test Client"
    assert str(mixer.blend(Client, client=client_name)) == client_name


def test_custom_queryset():
    mixer.blend(Client)  # This is just to ensure at least one client is in the DB for the queryset
    queryset = Client.objects.all()
    assert queryset.prefetch_related is not None
    assert "account_manager" in queryset._prefetch_related_lookups
