from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from clients.models import Client
from contracts.models import Contract


@receiver(post_save, sender=Client)
def update_contracts_status(sender, instance, **kwargs):
    if instance.is_lost:
        instance.client_contracts.update(contract_status="LOST")


# @receiver(pre_save, sender=Contract)
# def save_previous_supplier(sender, instance, **kwargs):
#     if instance.pk:
#         try:
#             # Get the current contract from the database
#             current_contract = Contract.objects.get(pk=instance.pk)
#             if current_contract.supplier != instance.supplier:
#                 # Save the current supplier to the previous_supplier field
#                 instance.previous_supplier = current_contract.supplier
#                 # Set the supplier_changed_date to the current date
#                 instance.supplier_changed_date = timezone.now().date()
#         except Contract.DoesNotExist:
#             # Handle the case where the contract does not exist
#             instance.previous_supplier = None
#             instance.supplier_changed_date = None


@receiver(pre_save, sender=Contract)  # noqa: E501
def save_previous_supplier(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Get the current contract from the database
            current_contract = Contract.objects.get(pk=instance.pk)
            if current_contract.supplier != instance.supplier:
                # Save the current supplier to the previous_supplier field
                instance.previous_supplier = current_contract.supplier
                # Check if supplier_changed_date is provided
                if not instance.supplier_changed_date:
                    raise ValidationError("Supplier changed date must be provided.")
        except Contract.DoesNotExist:
            # Handle the case where the contract does not exist
            instance.previous_supplier = None
            instance.supplier_changed_date = None
