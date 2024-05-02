import pytest
from django.core.exceptions import ValidationError
from clients.models import Client
from contacts.models import JobTitle, Contact
from users.models import AccountManager


# Fixtures
@pytest.fixture
def account_manager_instance(db):
    """Provides an AccountManager instance."""
    return AccountManager.objects.create(email="test1@example.com")


@pytest.fixture
def client_instance(db, account_manager_instance):
    """Provides a Client instance associated with an AccountManager."""
    return Client.objects.create(client="Test Client", account_manager=account_manager_instance)


@pytest.fixture
def job_title_instance(db):
    """Provides a JobTitle instance and verifies its string representation."""
    job_title = JobTitle.objects.create(title="Developer")
    assert str(job_title) == "Developer"
    return job_title


# Tests
@pytest.mark.django_db
def test_contact_str_representation(client_instance, job_title_instance):
    """Test the string representation of a Contact."""
    contact = Contact(
        client=client_instance,
        job_title=job_title_instance,
        email="test@example.com",
        name="John Doe",
        phone_number="123-456-7890",
    )
    contact.full_clean()
    contact.save()
    assert str(contact) == "John Doe - test@example.com"


@pytest.mark.django_db
def test_contact_invalid_email(client_instance, job_title_instance):
    """Test validation for an invalid email in a Contact."""
    contact = Contact(
        client=client_instance, job_title=job_title_instance, email="invalid-email", name="Jane Doe"
    )
    with pytest.raises(ValidationError):
        contact.full_clean()


@pytest.mark.django_db
def test_contact_optional_phone_number(client_instance, job_title_instance):
    """Test that the phone number is optional for a Contact."""
    contact = Contact(
        client=client_instance,
        job_title=job_title_instance,
        email="test@example.com",
        name="John Doe",
    )
    contact.full_clean()
    contact.save()
    assert contact.phone_number is None
