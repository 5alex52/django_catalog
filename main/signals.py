from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from pathlib import Path
from .models import Collection, Product, ProductImage, Category
import os
import shutil


BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

"""

Auto delete for Category

"""

@receiver(post_delete, sender=Category)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    shutil.rmtree(os.path.join(MEDIA_ROOT, 'category_{0}/'.format(instance.slug)), ignore_errors=True)


"""

Auto delete for Product

"""


@receiver(post_delete, sender=Product)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    shutil.rmtree(os.path.join(MEDIA_ROOT, 'category_{0}/product_{1}/'.format(
        instance.category.slug, instance.slug)), ignore_errors=True)


@receiver(pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).mainImage
    except sender.DoesNotExist:
        return False

    new_file = instance.mainImage
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


"""

Auto delete for Collection

"""


@receiver(post_delete, sender=Collection)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    shutil.rmtree(os.path.join(MEDIA_ROOT, 'collection_{}'.format(
        instance.slug)), ignore_errors=True)


@receiver(pre_save, sender=Collection)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


"""

Auto delete for ProductImage

"""


@receiver(post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=ProductImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
