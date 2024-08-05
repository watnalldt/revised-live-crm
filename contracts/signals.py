from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from clients.models import Client
from contracts.models import Contract
from django.utils import timezone


@receiver(post_save, sender=Client)
def update_contracts_status(sender, instance, **kwargs):
    if instance.is_lost and instance.export_confirmed:
        instance.client_contracts.update(contract_status="LOST")


@receiver(pre_save, sender=Contract)
def update_directors_approval_date(sender, instance, **kwargs):
    if instance.pk:  # Check if this is an existing instance
        try:
            old_instance = Contract.objects.get(pk=instance.pk)
            if old_instance.is_directors_approval != instance.is_directors_approval:
                instance.directors_approval_date = timezone.now()
        except Contract.DoesNotExist:
            pass  # Handle case where instance doesn't exist yet
    else:  # This is a new instance
        if instance.is_directors_approval == Contract.BaseYesNo.YES:
            instance.directors_approval_date = timezone.now()
