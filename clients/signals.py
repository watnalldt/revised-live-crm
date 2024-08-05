from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Client


@receiver(pre_save, sender=Client)
def update_client_lost_date(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # This is a new object, so field hasn't technically changed
        pass
    else:
        if obj.is_lost != instance.is_lost:
            if instance.is_lost:
                instance.client_lost_date = timezone.now().date()
            else:
                instance.client_lost_date = None
