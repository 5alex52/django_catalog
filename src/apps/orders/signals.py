from apps.orders.models import Order
from apps.utills import get_coordinates
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Order)
def do_something_if_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.delivery_address == instance.delivery_address:
            instance.latitude, instance.longitude = get_coordinates(
                instance.delivery_address
            )
