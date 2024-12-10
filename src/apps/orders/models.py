import uuid

from apps.main.models import Address
from apps.main.models import Product
from apps.main.services import get_full_url_to_product
from apps.utills import get_coordinates
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class PaymentMethodChoices(models.TextChoices):
    CASH = "Cash", _("Наличные")
    CARD = "Card", _("Картой")
    INSTALLMENT_PLAN = "Installment_plan", _("Рассрочка")
    CREDIT = "Credit", _("Кредит")


class StatusChoices(models.TextChoices):
    NEW = (
        "New",
        _("Новый"),
    )
    IN_PROGRESS = (
        "In progress",
        _("В процессе"),
    )
    COMPLETED = (
        "Completed",
        _("Завершён"),
    )
    CANCELLED = (
        "Cancelled",
        _("Отменён"),
    )


class DeliveryChoices(models.TextChoices):
    DELIVERY = (
        "Delivery",
        _("Доставка"),
    )
    PICKUP = "Pickup", _("Самовывоз")


class DeliveryStatusChoices(models.TextChoices):
    NEW = (
        "New",
        _("Новый"),
    )
    IN_PROGRESS = (
        "In progress",
        _("В процессе"),
    )
    COMPLETED = (
        "Completed",
        _("Завершён"),
    )
    CANCELLED = (
        "Cancelled",
        _("Отменён"),
    )


class Delivery(models.Model):
    status = models.CharField(
        "Статус доставки",
        max_length=20,
        blank=False,
        null=False,
        choices=DeliveryStatusChoices.choices,
        default="New",
    )
    created_at = models.DateField("Дата", auto_now_add=True)
    courier = models.CharField("Имя курьера", max_length=255, blank=False, null=False)
    shop_address = models.ForeignKey(
        Address,
        verbose_name="Магазин",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    total_distance = models.FloatField("Расстояние (км)", blank=True, null=True)

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"

    def __str__(self):
        return f"{self.courier} - {self.created_at}"


class Order(models.Model):
    session_id = models.UUIDField(editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    customer_first_name = models.CharField(
        "Имя", max_length=255, blank=False, null=False
    )
    customer_last_name = models.CharField(
        "Фамилия", max_length=255, blank=False, null=False
    )
    customer_email = models.EmailField("Email", blank=True, null=True)
    customer_phone = PhoneNumberField(
        "Номер телефона", blank=False, null=False, region="BY"
    )
    payment_method = models.CharField(
        "Метод оплаты",
        max_length=255,
        blank=False,
        null=False,
        choices=PaymentMethodChoices.choices,
    )
    delivery_method = models.CharField(
        "Метод доставки",
        max_length=255,
        blank=False,
        null=False,
        choices=DeliveryChoices.choices,
    )
    delivery_address = models.CharField(
        "Адрес доставки", max_length=255, blank=True, null=True
    )
    pickup_address = models.ForeignKey(
        Address,
        verbose_name="Адрес самовывоза",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        "Статус заказа",
        max_length=20,
        blank=False,
        null=False,
        choices=StatusChoices.choices,
        default="New",
    )

    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="orders", blank=True, null=True
    )

    def __str__(self):
        return f"Заказ {self.customer_first_name} {self.customer_last_name} {self.customer_phone}"

    @property
    def total_price(self):
        all_items = self.items.all()
        return sum(item.total_price for item in all_items)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self.latitude, self.longitude = get_coordinates(self.delivery_address)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"


class Cart(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    @property
    def total_price(self):
        all_items = self.items.all()
        return sum(item.total_price for item in all_items)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def link(self):
        return get_full_url_to_product(self.product)

    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"
