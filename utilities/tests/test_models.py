import pytest
from django.db import IntegrityError

from utilities.models import Supplier, Utility


@pytest.mark.django_db
def test_create_utility():
    utility = Utility.objects.create(utility="Test Utility")
    assert utility.utility == "Test Utility"


@pytest.mark.django_db
def test_create_supplier():
    supplier = Supplier.objects.create(supplier="Test Supplier")
    assert supplier.supplier == "Test Supplier"


@pytest.mark.django_db
def test_unique_constraint_utility():
    Utility.objects.create(utility="Test Utility")
    with pytest.raises(IntegrityError):
        Utility.objects.create(utility="Test Utility")  # This should raise an IntegrityError


@pytest.mark.django_db
def test_unique_constraint_supplier():
    Supplier.objects.create(supplier="Test Supplier")
    with pytest.raises(IntegrityError):
        Supplier.objects.create(supplier="Test Supplier")  # This should raise an IntegrityError


@pytest.mark.django_db
def test_utility_str_representation():
    # Test the string representation of the Utility model
    utility = Utility.objects.create(utility="Test Utility")

    assert str(utility) == utility.utility


@pytest.mark.django_db
def test_supplier_str_representation():
    # Test the string representation of the Supplier model
    supplier = Supplier.objects.create(supplier="Test Supplier")

    assert str(supplier) == supplier.supplier
