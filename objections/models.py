from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from clients.models import Client
from core.models import TimeStampedModel
from utilities.models import Supplier


class ObjectionsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "client",
                "objecting_supplier",
                "new_supplier",
            )
        )


class ObjectionQuerySet(models.QuerySet):
    def outstanding_objections(self):
        return self.filter(objection_status="OUTSTANDING").select_related(
            "client",
            "objecting_supplier",
            "new_supplier",
        )

    def pending_objections(self):
        return self.filter(objection_status="PENDING").select_related(
            "client",
            "objecting_supplier",
            "new_supplier",
        )


class Objection(TimeStampedModel):
    """This model replicates certain data as per the client's request"""

    class ObjectionStatus(models.TextChoices):
        OUTSTANDING = "OUTSTANDING", _("Outstanding")
        PENDING = "PENDING", _("Pending")
        RESOLVED = "RESOLVED", _("Resolved")

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name="Client Name",
        related_name="client_objections",
    )
    account_number = models.CharField(
        verbose_name="Account Number", max_length=100, null=True, blank=True
    )
    business_name = models.CharField(verbose_name="Business Name", max_length=255)
    site_address = models.TextField(verbose_name="Site Address")
    mpan_mpr = models.CharField(verbose_name="MPAN/MPR", max_length=255)
    new_supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        verbose_name="New Supplier",
        related_name="new_suppliers",
    )
    registration_date = models.DateField(verbose_name="Registration Date", null=True, blank=True)
    objection_date = models.DateField(verbose_name="Objection Date", null=True, blank=True)
    deadline_date = models.CharField(
        verbose_name="Deadline Date", max_length=25, null=True, blank=True
    )
    objecting_supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        verbose_name="Objecting Supplier",
        related_name="objecting_suppliers",
    )

    potential_start_date = models.CharField(
        verbose_name="Objection Date", max_length=25, null=True, blank=True
    )
    eac = models.IntegerField(verbose_name="EAC", null=True, blank=True)
    is_directors_approval = models.BooleanField(verbose_name="Directors Approval", default=False)
    objection_status = models.CharField(
        verbose_name="Objection Status",
        max_length=12,
        choices=ObjectionStatus.choices,
        default=ObjectionStatus.OUTSTANDING,
    )
    notes = models.TextField(null=True, blank=True)
    history = HistoricalRecords()

    objects = ObjectionsManager()  # Default Manager
    objections = ObjectionQuerySet.as_manager()  # Manager returns contracts on objection status

    class Meta:
        indexes = [
            models.Index(fields=["mpan_mpr"]),
            models.Index(fields=["client"]),
            models.Index(fields=["-client"]),
            models.Index(fields=["business_name"]),
            models.Index(fields=["-business_name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["mpan_mpr", "id"],
                name="unique_objection",
            )
        ]
        verbose_name = _("Contract Objection")
        verbose_name_plural = _("Contract Objections")

    def __str__(self):
        return str(self.client)
