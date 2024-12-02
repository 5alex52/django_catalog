import logging
import os
import shutil
from pathlib import Path

import telebot
from apps.utills import send_product_request
from apps.utills import send_product_to_telegram_channel
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_catalog.settings.env_config import env_config

from .models import Category
from .models import Collection
from .models import Feedback
from .models import Product

logger = logging.getLogger()


BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


@receiver(post_delete, sender=Category)
def auto_delete_category_folder_on_delete(sender, instance, **kwargs):
    """
    Auto delete for Category
    """
    shutil.rmtree(
        os.path.join(MEDIA_ROOT, "category_{0}/".format(instance.slug)),
        ignore_errors=True,
    )


@receiver(post_delete, sender=Product)
def auto_delete_product_folder_on_delete(sender, instance, **kwargs):
    """
    Auto delete for Product
    """
    shutil.rmtree(
        os.path.join(
            MEDIA_ROOT,
            "category_{0}/product_{1}/".format(instance.category.slug, instance.slug),
        ),
        ignore_errors=True,
    )


@receiver(post_delete, sender=Collection)
def auto_delete_collection_folder_on_delete(sender, instance, **kwargs):
    """
    Auto delete for Collection
    """
    shutil.rmtree(
        os.path.join(MEDIA_ROOT, "collection_{}".format(instance.slug)),
        ignore_errors=True,
    )


@receiver(post_save, sender=Feedback)
def send_notification_on_new_request(sender, instance, created, **kwargs):
    if created and env_config.ENVIROMENT == "production":
        bot = telebot.TeleBot(env_config.TECH_BOT_TOKEN, parse_mode=None)
        send_product_request(bot, instance)


@receiver(post_save, sender=Product)
def send_notification_on_new_product(sender, instance, created, **kwargs):
    if created and env_config.ENVIROMENT == "production":
        bot = telebot.TeleBot(env_config.TECH_BOT_TOKEN, parse_mode=None)
        send_product_to_telegram_channel(bot, instance)
