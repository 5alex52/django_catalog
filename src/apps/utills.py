import logging
from typing import Union

import requests
import telebot
from apps.main.models import Feedback
from apps.main.models import Product
from django.contrib.sites.models import Site
from django_catalog.settings.env_config import env_config
from yandex_geocoder import Client

logger = logging.getLogger()


def get_full_url_to_product(product: Product):
    domain = Site.objects.get_current().domain
    if env_config.ENVIROMENT == "production":
        protocol = "https"
    else:
        protocol = "http"
    return f"{protocol}://{domain}{product.get_absolute_url()}"


def send_product_to_telegram_channel(bot: telebot.TeleBot, product: Product):
    category = "\_".join(str(product.category).split(" "))

    base_message = (
        f"🆕 [{product.name}]({get_full_url_to_product(product)})\n\n"
        f"Производитель: {product.manufacturer.name}\n"
        f"{'Коллекция: ' + product.collection.name if product.collection else ''}"
        f"\nКатегория: #{category}\n\n"
        "Узнать цену и посмотреть характеристики можно на нашем сайте"
    )

    try:
        bot.send_photo(
            env_config.MAIN_CHANNEL_ID,
            photo=product.mainImage.url,
            caption=base_message,
            parse_mode="Markdown",
        )

        media = [
            telebot.types.InputMediaPhoto(photo.image.url)
            for photo in product.photos.all()
        ]

        if media:
            if len(media) == 1:
                bot.send_photo(env_config.MAIN_CHANNEL_ID, photo=media[0].media)
            else:
                bot.send_media_group(env_config.MAIN_CHANNEL_ID, media)
    except Exception as e:
        logger.warning(f"Ошибка при отправке сообщения: {e}")


def send_product_request(bot: telebot.TeleBot, feedback: Feedback):
    message = (
        f"📌 Заявка: \n\n👤 {feedback.name}"
        f"\n\n📞 `{feedback.phone}`\n\n"
        f"Товар: [{feedback.product.name}]({get_full_url_to_product(feedback.product)})"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(
        "Скопировать телефон(ПК)", callback_data=f"copy {feedback.phone}"
    )
    markup.add(button1)
    bot.send_message(
        env_config.TECH_CHANNEL_ID, message, parse_mode="MarkDown", reply_markup=markup
    )


def get_coordinates(address: str):
    """
    Получение координат по адресу.
    -> lat, lon
    """
    client = Client(env_config.YANDEX_MAPS_API_KEY)
    lon, lat = client.coordinates(address)
    return float(lat), float(lon)


def reorder_coordinates(coords: Union[tuple, list]) -> Union[tuple, list]:
    """
    Преобразует координаты

    lat, lon -> lon, lat
    lon, lat -> lat, lon
    """
    if isinstance(coords, tuple):
        return (coords[1], coords[0])
    elif isinstance(coords, list):
        return [(second, first) for first, second in coords]


def get_address_from_coordinates(orders, coord):
    for order in orders:
        if order.latitude == coord[1] and order.longitude == coord[0]:
            return order.delivery_address
    return "Не найден адрес"
