from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Форма для оформления заказа с поддержкой методов доставки и оплаты.
    """

    class Meta:
        model = Order
        fields = [
            "customer_first_name",
            "customer_last_name",
            "customer_email",
            "customer_phone",
            "payment_method",
            "delivery_method",
            "delivery_address",
            "pickup_address",
        ]
        widgets = {
            "customer_first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "first_name",
                    "placeholder": "Имя",
                }
            ),
            "customer_last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "last_name",
                    "placeholder": "Фамилия",
                }
            ),
            "customer_email": forms.EmailInput(
                attrs={"class": "form-control", "id": "email", "placeholder": "Email"}
            ),
            "customer_phone": forms.TextInput(
                attrs={"class": "form-control", "id": "phone", "placeholder": "Телефон"}
            ),
            "payment_method": forms.Select(
                attrs={"class": "form-control", "id": "payment_method"}
            ),
            "delivery_method": forms.Select(
                attrs={"class": "form-control", "id": "delivery_method"}
            ),
            "delivery_address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "delivery_address",
                    "placeholder": "Барановичи, Пролетарская 38А",
                }
            ),
            "pickup_address": forms.Select(
                attrs={"class": "form-control", "id": "pickup_address"}
            ),
        }

    def clean(self):
        """
        Дополнительная валидация полей.
        """
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get("delivery_method")
        delivery_address = cleaned_data.get("delivery_address")
        pickup_address = cleaned_data.get("pickup_address")

        import logging

        logger = logging.getLogger()

        logger.warning(delivery_method)
        logger.warning(delivery_address)

        if delivery_method == "Delivery" and not delivery_address:
            logger.warning("TEST TEST TEST")
            self.add_error("delivery_address", "Для доставки необходимо указать адрес.")
        elif delivery_method == "Pickup" and not pickup_address:
            self.add_error("pickup_address", "Для самовывоза необходимо выбрать адрес.")

        return cleaned_data
