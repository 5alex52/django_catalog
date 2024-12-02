from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from pathlib import Path
from .models import Collection, Product, Category
import os
import shutil


BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

"""

Auto delete for Category

"""


@receiver(post_delete, sender=Category)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    shutil.rmtree(
        os.path.join(MEDIA_ROOT, "category_{0}/".format(instance.slug)),
        ignore_errors=True,
    )


"""

Auto delete for Product

"""


@receiver(post_delete, sender=Product)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    shutil.rmtree(
        os.path.join(
            MEDIA_ROOT,
            "category_{0}/product_{1}/".format(instance.category.slug, instance.slug),
        ),
        ignore_errors=True,
    )


"""

Auto delete for Collection

"""


@receiver(post_delete, sender=Collection)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    shutil.rmtree(
        os.path.join(MEDIA_ROOT, "collection_{}".format(instance.slug)),
        ignore_errors=True,
    )
