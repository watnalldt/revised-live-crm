import pytest
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.test import Client
from contracts.models import Client as ContractClient, Contract
from django.test.utils import override_settings

User = get_user_model()


@pytest.fixture
def client_fixture(db):
    # It's a good practice to use db as a fixture dependency when your fixture interacts with the database.
    return ContractClient.objects.create(client="Test Client", account_manager_id=1)


@pytest.fixture
def contract_fixture(client_fixture):
    return Contract.objects.create(
        client=client_fixture, business_name="Test Business", amount=1000
    )


@pytest.fixture
def user_fixture(db):
    user = User.objects.create_user(email="testuser@example.com", password="password123")
    group = Group.objects.create(name="Account Managers")
    user.groups.add(group)
    return user


@pytest.fixture
def authenticated_client_fixture(user_fixture):
    with override_settings(AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"]):
        client = Client()
        client.login(email="testuser@example.com", password="password123")
        return client


@pytest.mark.django_db
def test_client_detail_view(authenticated_client_fixture, client_fixture):
    url = reverse("clients:client_detail", kwargs={"pk": client_fixture.pk})
    response = authenticated_client_fixture.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_contract_detail_view(authenticated_client_fixture, contract_fixture):
    url = reverse("clients:contract_detail", kwargs={"pk": contract_fixture.pk})
    response = authenticated_client_fixture.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_client_list_view(authenticated_client_fixture):
    url = reverse("clients:client_list")
    response = authenticated_client_fixture.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_clients_view(authenticated_client_fixture, client_fixture):
    url = reverse("clients:all_clients")
    response = authenticated_client_fixture.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_contracts_detail_view(authenticated_client_fixture, contract_fixture):
    url = reverse("clients:all_contracts_detail", kwargs={"pk": contract_fixture.pk})
    response = authenticated_client_fixture.get(url)
    assert response.status_code == 200
