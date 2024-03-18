import pytest
from django.urls import reverse
from mixer.backend.django import Mixer
from clients.models import Client

pytestmark = pytest.mark.django_db
mixer = Mixer()


def test_client_creation():
    client = mixer.blend(Client)
    assert isinstance(client, Client)


def test_client_absolute_url():
    client = mixer.blend(Client)
    url = reverse("clients:client_contracts", args=[str(client.pk)])
    assert client.get_absolute_url() == url


def test_client_str():
    client_name = "Test Client"
    client = mixer.blend(Client, client=client_name)
    assert str(client) == client_name


def test_custom_queryset():
    mixer.blend(Client)  # Ensure at least one client is in the DB for the queryset
    queryset = Client.objects.all()
    assert queryset.prefetch_related is not None
    assert "account_manager" in queryset._prefetch_related_lookups
