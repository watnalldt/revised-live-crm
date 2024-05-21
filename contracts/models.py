from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from clients.models import Client
from commissions.models import ElectricityCommission, GasCommission
from users.models import ClientManager
from utilities.models import Supplier, Utility


class ContractsManager(models.Manager):
    def get_queryset(self):
        """
        Override the default get_queryset method to include related objects in the query.

        Returns:
            QuerySet: A QuerySet instance that includes related 'client', 'client_manager',
            'supplier', and 'utility' objects for each contract.
        """
        return (
            super().get_queryset().select_related("client", "client_manager", "supplier", "utility")
        )


class UtilityQuerySet(models.QuerySet):
    def gas(self):
        """
        Filter the queryset to return only contracts related to gas utilities.

        Optimizes database queries by using select_related to include 'client', 'supplier', and
        'utility' objects in the query.

        Returns:
            QuerySet: A QuerySet instance of contracts filtered by gas utility.
        """
        return self.filter(utility__utility="Gas").select_related("client", "supplier", "utility")

    def electricity(self):
        """
        Filter the queryset to return only contracts related to electricity utilities.

        Optimizes database queries by using select_related to include 'client', 'supplier', and
        'utility' objects in the query.

        Returns:
            QuerySet: A QuerySet instance of contracts filtered by electricity utility.
        """
        return self.filter(utility__utility="Electricity").select_related(
            "client", "supplier", "utility"
        )


class ContractTypeQuerySet(models.QuerySet):
    def seamless(self):
        """
        Filter the queryset to return only contracts marked as 'SEAMLESS'.

        Optimizes database queries by using select_related to include 'client', 'supplier', and
        'utility' objects in the query.

        Returns:
            QuerySet: A QuerySet instance of contracts filtered by the seamless contract type.
        """
        return self.filter(contract_type="SEAMLESS").select_related("client", "supplier", "utility")

    def non_seamless(self):
        """
        Filter the queryset to return only contracts marked as 'NON-SEAMLESS'.

        Optimizes database queries by using select_related to include 'client', 'supplier', and
        'utility' objects in the query.

        Returns:
            QuerySet: A QuerySet instance of contracts filtered by the non-seamless contract type.
        """
        return self.filter(contract_type="NON_SEAMLESS").select_related(
            "client", "supplier", "utility"
        )


class Contract(models.Model):
    class BaseYesNo(models.TextChoices):
        YES = "YES", _("Yes")
        NO = "NO", _("No")

    class VatRate(models.TextChoices):
        FIVE_PERCENT = "5%", "5%"
        TWENTY_PERCENT = "20%", "20%"
        UNKNOWN = "UNKNOWN", "Unknown"

    class ContractType(models.TextChoices):
        SEAMLESS = "SEAMLESS", _("Seamless")
        NON_SEAMLESS = "NON_SEAMLESS", _("Non-Seamless")

    class ContractStatus(models.TextChoices):
        LIVE = "LIVE", _("Live")
        REMOVED = "REMOVED", _("Removed")
        LOCKED = "LOCKED", _("Locked")
        PRICING = "PRICING", _("Pricing")
        OBJECTION = "OBJECTION", _("Objection")
        NEW = "NEW", _("New")
        LOST = "LOST", _("Lost")
        EXPIRED = "EXPIRED", _("Expired")
        FUTURE = "FUTURE", _("Future")
        CONTRACT_REQUESTED = "CONTRACT_REQUESTED", _("Contract Requested")
        AWAITING_DA = "AWAITING_DA", _("Awaiting DA")
        DUPLICATE = "DUPLICATE", _("Duplicate")
        IN_SUPPLIER_BACKLOG = "IN_SUPPLIER_BACKLOG", _("In Supplier Backlog")
        DATA_CLEANSE = "DATA_CLEANSE", _("Data Cleanse")

    class MeterStatus(models.TextChoices):
        """The default is set to Active"""

        ACTIVE = "ACTIVE", _("Active")
        DE_ENERGISED = "DE_ENERGISED", _("De-Energised")
        REMOVED = "REMOVED", _("Removed")

    client_manager = models.ForeignKey(
        ClientManager,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Client Manager",
        related_name="client_manager_contracts",
    )

    contract_type = models.CharField(
        max_length=20, choices=ContractType.choices, default=ContractType.SEAMLESS
    )
    seamless_updated = models.CharField(
        verbose_name="Seamless Contract Updated",
        choices=BaseYesNo.choices,
        default=BaseYesNo.NO,
    )
    contract_status = models.CharField(
        max_length=20, choices=ContractStatus.choices, default=ContractStatus.LIVE
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Client Name",
        related_name="client_contracts",
    )
    client_group = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Client Group"
    )
    is_directors_approval = models.CharField(
        verbose_name="Directors Approval",
        choices=BaseYesNo.choices,
        default=BaseYesNo.NO,
    )
    business_name = models.CharField(verbose_name="Business Name", max_length=255)
    company_reg_number = models.CharField(
        verbose_name="Company Reg Number", max_length=250, null=True, blank=True
    )
    utility = models.ForeignKey(
        Utility,
        on_delete=models.CASCADE,
        verbose_name="Utility Type",
        related_name="contract_utilities",
    )
    top_line = models.CharField(verbose_name="Top Line", max_length=40, null=True, blank=True)
    mpan_mpr = models.CharField(verbose_name="MPAN/MPR", max_length=255)
    meter_serial_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text=mark_safe(
            "<a href='https://www.ecoes.co.uk' target='_blank'>" "Look up Meter Serial Number</a>"
        ),
    )
    meter_onboarded = models.DateField(verbose_name="Meter On Boarded", null=True, blank=True)
    meter_status = models.CharField(
        verbose_name="Meter Status",
        choices=MeterStatus.choices,
        default=MeterStatus.ACTIVE,
        max_length=25,
    )
    building_name = models.CharField(
        verbose_name="Building Name", max_length=255, null=True, blank=True
    )
    site_address = models.TextField(verbose_name="Site Address", null=True, blank=True)
    billing_address = models.CharField(
        verbose_name="Billing Address", max_length=255, null=True, blank=True
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name="Supplier Name",
        related_name="contract_suppliers",
    )
    supplier_coding = models.CharField(max_length=50, null=True, blank=True)
    contract_start_date = models.DateField(
        verbose_name="Contract Start Date", null=True, blank=True
    )
    contract_end_date = models.DateField(verbose_name="Contract End Date", null=True, blank=True)
    lock_in_date = models.DateField(verbose_name="Lock In Date", null=True, blank=True)
    supplier_start_date = models.DateField(
        verbose_name="Supplier Start Date", null=True, blank=True
    )
    account_number = models.CharField(
        verbose_name="Account Number", max_length=100, null=True, blank=True
    )
    eac = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    day_consumption = models.FloatField(verbose_name="Day Consumption", null=True, blank=True)
    night_consumption = models.FloatField(verbose_name="Night Consumption", null=True, blank=True)
    kva = models.CharField(verbose_name="KVA", max_length=25, null=True, blank=True)
    vat_rate = models.CharField(
        verbose_name="VAT Rate",
        choices=VatRate.choices,
        default=VatRate.UNKNOWN,
        max_length=30,
    )
    contract_value = models.DecimalField(
        verbose_name="Contract Value",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    standing_charge = models.DecimalField(
        verbose_name="Standing Charge",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    sc_frequency = models.CharField(
        verbose_name="Standing Charge Frequency", max_length=250, null=True, blank=True
    )
    unit_rate_1 = models.DecimalField(
        verbose_name="Unit Rate 1",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    unit_rate_2 = models.DecimalField(
        verbose_name="Unit Rate 2",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    unit_rate_3 = models.DecimalField(
        verbose_name="Unit Rate 3",
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    feed_in_tariff = models.DecimalField(
        verbose_name="Feed In Tariff",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    seamless_status = models.CharField(
        verbose_name="Seamless Status", max_length=50, null=True, blank=True
    )
    profile = models.CharField(verbose_name="Profile", max_length=100, null=True, blank=True)
    is_ooc = models.CharField(
        verbose_name="Out Of Contract",
        choices=BaseYesNo.choices,
        default=BaseYesNo.NO,
    )
    service_type = models.CharField(max_length=50, null=True, blank=True)

    pence_per_kilowatt = models.DecimalField(
        verbose_name="Pence Per Kilowatt",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    day_kilowatt_hour_rate = models.DecimalField(
        verbose_name="Day Kilowatt Hour Rate",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
    )
    night_rate = models.DecimalField(
        verbose_name="Night Rate", max_digits=8, decimal_places=8, null=True, blank=True
    )
    annualised_budget = models.DecimalField(
        verbose_name="Annualised Budget",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    commission_per_annum = models.DecimalField(
        verbose_name="Commission Per Annum",
        editable=False,
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    commission_per_unit = models.DecimalField(
        verbose_name="Commission Per Unit",
        editable=False,
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    commission_per_contract = models.DecimalField(
        verbose_name="Commission Per Contract",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    partner_commission = models.DecimalField(
        verbose_name="Partner Commission",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    smart_meter = models.CharField(verbose_name="Smart Meter", max_length=50, null=True, blank=True)
    vat_declaration_sent = models.CharField(
        verbose_name="Vat Declaration Sent",
        choices=BaseYesNo.choices,
        default=BaseYesNo.NO,  # Setting default value to NO
    )
    vat_declaration_date = models.DateField(verbose_name="Date Sent", blank=True, null=True)
    vat_declaration_expires = models.DateField(
        verbose_name="Vat Declaration Expiry Date", null=True, blank=True
    )
    notes = models.TextField(null=True, blank=True)
    # future_contract_start_date = models.DateField(
    #     verbose_name="Future Contract Start Date", null=True, blank=True
    # )
    #
    # future_contract_end_date = models.DateField(
    #     verbose_name="Future Contract End Date", null=True, blank=True
    # )
    # future_unit_rate_1 = models.DecimalField(
    #     verbose_name="Future Unit Rate 1",
    #     max_digits=9,
    #     decimal_places=6,
    #     null=True,
    #     blank=True,
    # )
    # future_unit_rate_2 = models.DecimalField(
    #     verbose_name="Future Unit Rate 2",
    #     max_digits=9,
    #     decimal_places=6,
    #     null=True,
    #     blank=True,
    # )
    # future_unit_rate_3 = models.DecimalField(
    #     verbose_name="Future Unit Rate 3",
    #     max_digits=9,
    #     decimal_places=6,
    #     null=True,
    #     blank=True,
    # )
    #
    # future_supplier = models.ForeignKey(
    #     Supplier,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     verbose_name="Future Supplier",
    #     related_name="future_suppliers",
    # )
    # future_standing_charge = models.DecimalField(
    #     verbose_name="Future Standing Charge",
    #     max_digits=8,
    #     decimal_places=4,
    #     null=True,
    #     blank=True,
    # )
    history = HistoricalRecords()

    objects = ContractsManager()  # Default Manager
    utilities = UtilityQuerySet.as_manager()  # Manager returns contracts per utility
    contracts = ContractTypeQuerySet.as_manager()

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
                name="unique_contract",
            )
        ]
        db_table = "client_contracts"
        permissions = [
            (
                "can_export_commissions",
                "Can export commissions",
            ),
            ("can_access_bulk_quote_template", "Can access bulk quote template"),
        ]
        verbose_name = _("Client Contract")
        verbose_name_plural = _("Client Contracts")
        ordering = ["contract_end_date"]

    def __str__(self):
        return f"{self.business_name} with mpan {self.mpan_mpr}"

    def calculate_commission(self):
        """Calculate and set commission rates based on utility type."""
        commission_model = None

        if self.utility.utility == "Electricity":
            commission_model = ElectricityCommission
        elif self.utility.utility == "Gas":
            commission_model = GasCommission

        if commission_model:
            commission = commission_model.objects.filter(
                eac_from__lte=self.eac, eac_to__gte=self.eac, client=self.client
            ).first()

            if commission:
                self.commission_per_annum = commission.commission_per_annum
                self.commission_per_unit = commission.commission_per_unit

    def validate_vat_declaration(self):
        """Validate VAT declaration and set appropriate values."""
        if self.vat_declaration_sent == self.BaseYesNo.YES:
            if self.vat_declaration_date is None:
                raise ValidationError(
                    "Error: vat_declaration_date cannot be null when vat_declaration_sent is YES."
                )
            self.vat_declaration_expires = self.contract_end_date
        else:
            self.vat_declaration_expires = None

        if self.vat_rate not in [
            self.VatRate.FIVE_PERCENT,
            self.VatRate.TWENTY_PERCENT,
            self.VatRate.UNKNOWN,
        ]:
            raise ValidationError("Invalid VAT rate")

    def save(self, *args, **kwargs):
        self.calculate_commission()  # Calculate commission before saving
        self.validate_vat_declaration()  # Validate VAT declaration

        self.full_clean()  # Call the clean method before saving
        super().save(*args, **kwargs)  # Call the original save method to save the model

    # Returns the number of days left on the contract

    @property
    def days_till(self):
        today = date.today()
        days_till = self.contract_end_date - today
        return str(days_till).split(",", 1)[0]

    # Contract Term used in bulk upload template
    @property
    def contract_term(self):
        return self.client.contract_term
