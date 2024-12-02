import logging

import telebot
from apps.main.models import Feedback
from apps.main.models import Product
from django.contrib.sites.models import Site
from django_catalog.settings.env_config import env_config

logger = logging.getLogger()


def get_full_url_to_product(product: Product):
    domain = Site.objects.get_current().domain
    return f"https://{domain}{product.get_absolute_url()}"


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
