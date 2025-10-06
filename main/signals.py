import os
import shutil
from pathlib import Path

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Category, Feedback
from .models import Collection
from .models import Product

import telebot
from .services import send_product_request
from .services import send_product_to_telegram_channel
from django_catalog.settings import DEBUG, TECH_BOT_TOKEN


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


@receiver(post_save, sender=Feedback)
def send_notification_on_new_request(sender, instance, created, **kwargs):
    if created and not DEBUG:
        bot = telebot.TeleBot(TECH_BOT_TOKEN, parse_mode=None)
        send_product_request(bot, instance)


@receiver(post_save, sender=Product)
def send_notification_on_new_product(sender, instance, created, **kwargs):
    if created and not DEBUG:
        bot = telebot.TeleBot(TECH_BOT_TOKEN, parse_mode=None)
        send_product_to_telegram_channel(bot, instance)