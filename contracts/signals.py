from django.db.models.signals import post_save
from django.dispatch import receiver

from clients.models import Client


@receiver(post_save, sender=Client)
def update_contracts_status(sender, instance, **kwargs):
    if instance.is_lost:
        instance.client_contracts.update(contract_status="LOST")
