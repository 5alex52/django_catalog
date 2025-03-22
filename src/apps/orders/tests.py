import random
from datetime import datetime
from datetime import timedelta
from unittest.mock import MagicMock

import pytest
from conftest import CartFactory
from conftest import OrderFactory
from conftest import OrderItemFactory
from conftest import ProductFactory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from .services import DateTimeService
from .services import MetricsService
from .services import MetricsTotalService
from .services import MetricsVisualService


# Тестирование метода current_week
def test_current_week(mock_now):
    # Предположим, что сегодня понедельник 2024-12-09
    mock_now.return_value = datetime(2024, 12, 9, 12, 0)

    start, end = DateTimeService.current_week()

    assert start == datetime(2024, 12, 9).date()  # Понедельник
    assert end == datetime(2024, 12, 15).date()  # Воскресенье


# Тестирование метода current_month
def test_current_month(mock_now):
    # Предположим, что сегодня 2024-12-09
    mock_now.return_value = datetime(2024, 12, 9, 12, 0)

    start, end = DateTimeService.current_month()

    assert start == datetime(2024, 12, 1).date()  # 1 декабря
    assert end == datetime(2024, 12, 31).date()  # 31 декабря


# Тестирование метода previous_week
def test_previous_week(mock_now):
    # Предположим, что сегодня 2024-12-09
    mock_now.return_value = datetime(2024, 12, 9, 12, 0)

    start, end = DateTimeService.previous_week()

    assert start == datetime(2024, 12, 2).date()  # Понедельник прошлой недели
    assert end == datetime(2024, 12, 8).date()  # Воскресенье прошлой недели


# Тестирование метода is_date_in_range
def test_is_date_in_range():
    date = datetime(2024, 12, 9).date()
    start_date = datetime(2024, 12, 1).date()
    end_date = datetime(2024, 12, 31).date()

    assert DateTimeService.is_date_in_range(date, start_date, end_date) is True
    assert (
        DateTimeService.is_date_in_range(
            datetime(2024, 11, 30).date(), start_date, end_date
        )
        is False
    )


def test_generate_kpi_from_template(metrics_visual_service: MetricsVisualService):
    # Подготовка данных
    title = "Выручка"
    metric = 1000.50
    dates = ["Пн", "Вт", "Ср", "Чт", "Пт"]
    values = [200, 300, 150, 250, 100]
    footer = 5.5
    label = "Текущая неделя"

    # Вызов метода
    result = metrics_visual_service.generate_kpi_from_template(
        title, metric, dates, values, footer, label
    )

    # Проверки
    assert "title" in result
    assert result["title"] == title
    assert "metric" in result
    assert result["metric"] == "1,000.5 BYN"  # Проверка форматирования
    assert "chart" in result
    assert "footer" in result
    assert "label" in result


def test_generate_progress_from_template(metrics_visual_service: MetricsVisualService):
    dataset = [
        {"title": "Продукт A", "description": 5500.75, "value": 30},
        {"title": "Продукт B", "description": 300.25, "value": 50},
    ]

    result = metrics_visual_service.generate_progress_from_template(dataset)

    # Проверки
    assert len(result) == 2
    assert result[0]["title"] == "Продукт A"
    assert result[0]["description"] == "5,500.75 BYN"
    assert result[1]["value"] == 50


class MetricsServiceTest(TestCase):
    def setUp(self):
        # Генерация случайных продуктов и заказов
        self.create_test_data()

        # Инициализация сервисов для метрик
        self.metrics_service = MetricsService()
        self.metrics_total_service = MetricsTotalService()

    def create_test_data(self):
        """Создаёт случайные тестовые продукты и заказы."""
        # Создаём 5 случайных продуктов
        self.products = ProductFactory.create_batch(5)

        # Создаём 3 случайных заказа за последние 7 дней
        for _ in range(3):
            order = OrderFactory(
                created_at=timezone.now() - timedelta(days=random.randint(1, 7))
            )
            # Добавляем случайное количество позиций в заказ
            for _ in range(random.randint(1, 3)):
                OrderItemFactory(
                    order=order,
                    product=random.choice(self.products),
                    quantity=random.randint(1, 5),
                )

    def test_get_total_revenue_by_week(self):
        """Тест получения общей выручки за неделю."""
        start = timezone.now() - timedelta(weeks=1)
        end = timezone.now()
        revenue = self.metrics_service.get_total_revenue_by_period(start, end)

        # Проверка, что выручка больше 0
        self.assertGreater(revenue, 0)

    def test_get_total_revenue_by_month(self):
        """Тест получения общей выручки за месяц."""
        start = timezone.now() - timedelta(weeks=4)
        end = timezone.now()
        revenue = self.metrics_service.get_total_revenue_by_period(start, end)

        # Проверка, что выручка больше 0
        self.assertGreater(revenue, 0)

    def test_get_revenue_share_by_product_for_week(self):
        """Тест получения доли выручки по продуктам за неделю."""
        start, end = DateTimeService.current_week()
        revenue_share = self.metrics_service.get_revenue_share_by_product(start, end)

        # Проверка, что количество записей в отчёте равно количеству продуктов
        self.assertTrue(len(revenue_share) > 0)


@pytest.mark.django_db
def test_list_cart(api_client, mock_get_cart):
    url = reverse("cart-list")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    mock_get_cart.assert_called_once()


@pytest.mark.django_db
def test_add_product_to_cart(api_client, mock_get_cart: MagicMock):

    test_product = ProductFactory.create()
    test_cart = CartFactory.create(id=1)
    url = reverse("cart-add", args=[test_product.id])

    response = api_client.post(url)

    mock_get_cart.assert_called_once()
    assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post(url)

    url = reverse("cart-list")

    response = api_client.get(url)
    import logging

    logger = logging.getLogger()

    logger.warning(response.data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == 1
    assert response.data["items"][0]["quantity"] == 2


@pytest.mark.django_db
def test_remove_product_from_cart(api_client, mock_get_cart):
    test_product = ProductFactory.create()
    test_cart = CartFactory.create(id=1)
    url = reverse("cart-remove", args=[test_product.id])

    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    mock_get_cart.assert_called_once()
