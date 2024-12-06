import random
import uuid  # Импортируем модуль uuid для генерации уникальных идентификаторов
from datetime import datetime
from datetime import timedelta

from apps.main.models import Address
from apps.orders.models import DeliveryChoices
from apps.orders.models import Order
from apps.orders.models import OrderItem
from apps.orders.models import PaymentMethodChoices
from apps.orders.models import Product
from django.utils.timezone import make_aware
from phonenumber_field.modelfields import PhoneNumberField


# Функция для генерации случайных данных
def generate_random_orders():
    # Создание случайных заказов для текущего и прошлого периода
    products = Product.objects.filter(id__in=[1, 9, 10, 11])  # Фильтрация по товарам
    statuses = ["New", "In progress", "Completed", "Cancelled"]

    # Генерация случайных заказов для текущей недели
    current_week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    current_week_end = current_week_start + timedelta(days=6)

    # Генерация случайных заказов для предыдущей недели
    previous_week_start = current_week_start - timedelta(weeks=1)
    previous_week_end = previous_week_start + timedelta(days=6)

    # Генерация случайных заказов для текущего месяца
    current_month_start = datetime(datetime.now().year, datetime.now().month, 1)
    next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
    current_month_end = next_month_start - timedelta(days=1)

    # Генерация случайных заказов для предыдущего месяца
    previous_month_end = current_month_start - timedelta(days=1)
    previous_month_start = datetime(
        previous_month_end.year, previous_month_end.month, 1
    )

    # Генерация случайных заказов для текущего года
    current_year_start = datetime(datetime.now().year, 1, 1)
    current_year_end = datetime(datetime.now().year, 12, 31)

    # Генерация случайных заказов для прошлого года
    previous_year_start = datetime(datetime.now().year - 1, 1, 1)
    previous_year_end = datetime(datetime.now().year - 1, 12, 31)

    # Создаем заказы для разных периодов
    periods = [
        ("current_week", current_week_start, current_week_end),
        ("previous_week", previous_week_start, previous_week_end),
        ("current_month", current_month_start, current_month_end),
        ("previous_month", previous_month_start, previous_month_end),
        ("current_year", current_year_start, current_year_end),
        ("previous_year", previous_year_start, previous_year_end),
    ]

    for period_name, period_start, period_end in periods:
        order = Order.objects.create(
            session_id=uuid.uuid4(),  # Используем правильный uuid для генерации
            created_at=make_aware(random_date_in_period(period_start, period_end)),
            customer_first_name=f"Имя{random.randint(1, 100)}",
            customer_last_name=f"Фамилия{random.randint(1, 100)}",
            customer_email=f"test{random.randint(1, 100)}@mail.com",
            customer_phone=PhoneNumberField(region="BY").to_python(f"+375291234567"),
            payment_method=random.choice(
                [choice[0] for choice in PaymentMethodChoices.choices]
            ),
            delivery_method=random.choice(
                [choice[0] for choice in DeliveryChoices.choices]
            ),
            delivery_address=f"Адрес {random.randint(1, 100)}",
            pickup_address=None,  # Можете установить случайный адрес, если есть
            status=random.choice(statuses),
        )

        # Создаем товар для каждого заказа
        for _ in range(
            random.randint(1, 3)
        ):  # Каждый заказ может содержать от 1 до 3 товаров
            product = random.choice(products)
            OrderItem.objects.create(
                order=order, product=product, quantity=random.randint(1, 5)
            )


# Генерация случайной даты в пределах заданного периода
def random_date_in_period(start_date, end_date):
    time_delta = end_date - start_date
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)
