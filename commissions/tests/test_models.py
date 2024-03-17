import pytest
from decimal import Decimal

from clients.models import Client
from users.models import AccountManager
from ..models import ElectricityCommission, GasCommission


@pytest.fixture
def account_manager():
    return AccountManager.objects.create(email="testuser@example.com")  # Adjust as necessary


# Modify the client fixture to accept the account_manager fixture as an argument
@pytest.fixture
def client(account_manager):
    # Use the account_manager directly as it now refers to an AccountManager instance returned by the fixture
    return Client.objects.create(
        client="Test Client", account_manager=account_manager
    )  # Adjust based on the Client model's fields


@pytest.mark.django_db
def test_electricity_commission_str(client):
    ec = ElectricityCommission.objects.create(
        client=client,
        eac_from=Decimal("1000.00"),
        eac_to=Decimal("2000.00"),
        commission_per_annum=Decimal("150.00"),
        commission_per_unit=Decimal("0.015"),
    )
    assert str(ec) == "1000.00 - 2000.00 for Electricity Contracts"


@pytest.mark.django_db
def test_gas_commission_str(client):
    gc = GasCommission.objects.create(
        client=client,
        eac_from=Decimal("500.00"),
        eac_to=Decimal("1500.00"),
        commission_per_annum=Decimal("100.00"),
        commission_per_unit=Decimal("0.010"),
    )
    assert str(gc) == "500.00 - 1500.00 for Gas Contracts"


@pytest.mark.django_db
def test_electricity_commission_fields(client):
    ec = ElectricityCommission.objects.create(
        client=client,
        eac_from=Decimal("1000.00"),
        eac_to=Decimal("2000.00"),
        commission_per_annum=Decimal("150.00"),
        commission_per_unit=Decimal("0.015"),
    )
    assert ec.client == client
    assert ec.eac_from == Decimal("1000.00")
    assert ec.eac_to == Decimal("2000.00")
    assert ec.commission_per_annum == Decimal("150.00")
    assert ec.commission_per_unit == Decimal("0.015")


@pytest.mark.django_db
def test_gas_commission_fields(client):
    gc = GasCommission.objects.create(
        client=client,
        eac_from=Decimal("500.00"),
        eac_to=Decimal("1500.00"),
        commission_per_annum=Decimal("100.00"),
        commission_per_unit=Decimal("0.010"),
    )
    assert gc.client == client
    assert gc.eac_from == Decimal("500.00")
    assert gc.eac_to == Decimal("1500.00")
    assert gc.commission_per_annum == Decimal("100.00")
    assert gc.commission_per_unit == Decimal("0.010")
