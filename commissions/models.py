from django.db import models
from django.utils.translation import gettext_lazy as _

from clients.models import Client


class ElectricityCommission(models.Model):
    """
    Represents an electricity commission for a client, including details about
    estimated annual consumption (EAC) ranges and commission rates.
    """

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="electricity_commissions"
    )
    eac_from = models.DecimalField(max_digits=10, decimal_places=2)
    eac_to = models.DecimalField(max_digits=10, decimal_places=2)
    commission_per_annum = models.DecimalField(max_digits=10, decimal_places=2)
    commission_per_unit = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        verbose_name = _("Electricity Commission")
        verbose_name_plural = _("Electricity Commissions")

    def __str__(self):
        return f"{self.eac_from} - {self.eac_to} for Electricity Contracts"


class GasCommission(models.Model):
    """
    Represents a gas commission for a client, detailing the estimated annual
    consumption (EAC) ranges and commission rates similarly to electricity commissions.
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="gas_commissions")
    eac_from = models.DecimalField(max_digits=10, decimal_places=2)
    eac_to = models.DecimalField(max_digits=10, decimal_places=2)
    commission_per_annum = models.DecimalField(max_digits=10, decimal_places=3)
    commission_per_unit = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        verbose_name = _("Gas Commission")
        verbose_name_plural = _("Gas Commissions")

    def __str__(self):
        return f"{self.eac_from} - {self.eac_to} for Gas Contracts"
