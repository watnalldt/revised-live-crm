from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from core.models import TimeStampedModel
from users.models import AccountManager


class ClientsManager(models.Manager):
    def get_queryset(self):
        """
        Overrides the default queryset to prefetch related account_manager objects.

        This optimization is used to reduce the number of queries to the database
        when accessing the account_manager field of a Client instance.

        Returns:
            QuerySet: A QuerySet instance which prefetches related account_manager objects.
        """
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "account_manager",
            )
        )


class Client(TimeStampedModel):
    """
    Represents a client in the system, extending TimeStampedModel to include
    creation and modification timestamps automatically.
    """

    client = models.CharField(verbose_name="Client", max_length=255, unique=True)
    account_manager = models.ForeignKey(
        AccountManager,
        on_delete=models.CASCADE,
        verbose_name="Account Manager",
        related_name="account_manager_clients",
    )
    originator = models.CharField(max_length=250, null=True, blank=True, verbose_name="Originator")
    client_onboarded = models.DateField(null=True, blank=True, verbose_name="Client Onboarded")
    loa = models.DateField(verbose_name="Letter of Authority", null=True, blank=True)
    contract_term = models.CharField(max_length=250, null=True, blank=True, verbose_name="Contract Term")
    is_lost = models.BooleanField(
        default=False,
        verbose_name="Lost Client",
    )
    notes = models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    objects = ClientsManager()

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["client"]

    def __str__(self):
        return self.client

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this client."""
        return reverse("clients:client_contracts", args=[str(self.pk)])
