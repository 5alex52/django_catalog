import json
import logging
from calendar import monthrange
from collections.abc import Callable
from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.cache import caches
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Count
from django.db.models import F
from django.db.models import QuerySet
from django.db.models import Sum
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from .models import Order

CACHE_TIMEOUTS = {
    "5_seconds": 5,
    "5_minutes": 5 * 60,  # 5 минут (в секундах)
    "10_minutes": 10 * 60,  # 10 минут (в секундах)
    "1_hour": 60 * 60,  # 1 час (в секундах)
    "6_hours": 6 * 60 * 60,  # 6 часов (в секундах)
    "12_hours": 12 * 60 * 60,  # 12 часов (в секундах)
    "1_day": 24 * 60 * 60,  # 1 день (в секундах)
}

METRICS_CACHE_TIMEOUTS = {
    "total_revenue_by_week": CACHE_TIMEOUTS["5_minutes"],
    "total_revenue_by_month": CACHE_TIMEOUTS["10_minutes"],
    "total_revenue_by_quarter": CACHE_TIMEOUTS["12_hours"],
    "total_revenue_by_year": CACHE_TIMEOUTS["1_day"],
    "total_revenue_growth_by_week": CACHE_TIMEOUTS["5_minutes"],
    "total_revenue_growth_by_month": CACHE_TIMEOUTS["10_minutes"],
    "total_revenue_growth_by_quarter": CACHE_TIMEOUTS["12_hours"],
    "total_revenue_growth_by_year": CACHE_TIMEOUTS["1_day"],
    "total_orders_by_week": CACHE_TIMEOUTS["5_minutes"],
    "total_orders_by_month": CACHE_TIMEOUTS["10_minutes"],
    "weekly_revenue": CACHE_TIMEOUTS["5_minutes"],
    "monthly_revenue": CACHE_TIMEOUTS["10_minutes"],
    "quarterly_revenue": CACHE_TIMEOUTS["12_hours"],
    "yearly_revenue": CACHE_TIMEOUTS["1_day"],
}


redis_cache = caches["redis"]

logger = logging.getLogger()


class DateTimeService:
    """Сервис для работы с датами и временем."""

    @staticmethod
    def current_week():
        """Возвращает начало и конец текущей недели."""
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Понедельник
        end_of_week = start_of_week + timedelta(days=6)  # Воскресенье
        return start_of_week, end_of_week

    @staticmethod
    def current_month():
        """Возвращает начало и конец текущего месяца."""
        today = now().date()
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(
            day=monthrange(today.year, today.month)[1]
        )  # Последний день месяца
        return start_of_month, end_of_month

    @staticmethod
    def previous_week():
        """Возвращает начало и конец прошлой недели."""
        today = now().date()
        start_of_current_week = today - timedelta(
            days=today.weekday()
        )  # Понедельник текущей недели
        end_of_last_week = start_of_current_week - timedelta(
            days=1
        )  # Воскресенье прошлой недели
        start_of_last_week = end_of_last_week - timedelta(
            days=6
        )  # Понедельник прошлой недели
        return start_of_last_week, end_of_last_week

    @staticmethod
    def previous_month():
        """Возвращает начало и конец прошлого месяца."""
        today = now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        start_of_previous_month = last_day_of_previous_month.replace(day=1)
        return start_of_previous_month, last_day_of_previous_month

    @staticmethod
    def current_day():
        """Возвращает начало и конец текущего дня."""
        today = now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        return start_of_day, end_of_day

    @staticmethod
    def previous_day():
        """Возвращает начало и конец предыдущего дня."""
        today = now().date()
        yesterday = today - timedelta(days=1)
        start_of_day = datetime.combine(yesterday, datetime.min.time())
        end_of_day = datetime.combine(yesterday, datetime.max.time())
        return start_of_day, end_of_day

    @staticmethod
    def is_date_in_range(date, start_date, end_date):
        """Проверяет, входит ли дата в диапазон."""
        return start_date <= date <= end_date

    @staticmethod
    def current_quarter():
        """Возвращает начало и конец текущего квартала."""
        today = now().date()
        quarter = (today.month - 1) // 3 + 1
        start_month = 3 * (quarter - 1) + 1
        end_month = start_month + 2
        start_of_quarter = today.replace(month=start_month, day=1)
        end_of_quarter = today.replace(
            month=end_month, day=monthrange(today.year, end_month)[1]
        )
        return start_of_quarter, end_of_quarter

    @staticmethod
    def previous_quarter():
        today = now().date()
        quarter = (today.month - 1) // 3 + 1
        start_month = 3 * (quarter - 2) + 1
        end_month = start_month + 2
        start_of_quarter = today.replace(month=start_month, day=1)
        end_of_quarter = today.replace(
            month=end_month, day=monthrange(today.year, end_month)[1]
        )
        return start_of_quarter, end_of_quarter

    @staticmethod
    def custom_date_range(start_date, end_date):
        """Возвращает диапазон между двумя произвольными датами."""
        return datetime.combine(start_date, datetime.min.time()), datetime.combine(
            end_date, datetime.max.time()
        )

    @staticmethod
    def current_year():
        """Возвращает начало и конец текущего года."""
        today = now().date()
        start_of_year = today.replace(month=1, day=1)
        end_of_year = today.replace(month=12, day=31)
        return start_of_year, end_of_year

    @staticmethod
    def previous_year():
        """Возвращает начало и конец предыдущего года."""
        today = now().date()
        start_of_last_year = today.replace(year=today.year - 1, month=1, day=1)
        end_of_last_year = today.replace(year=today.year - 1, month=12, day=31)
        return start_of_last_year, end_of_last_year

    @staticmethod
    def last_n_days(n):
        """Возвращает начало и конец диапазона за последние N дней."""
        end_date = now()
        start_date = end_date - timedelta(days=n)
        return start_date, end_date


class MetricsVisualService:
    def __init__(self):
        self.MetricsTotalService = MetricsTotalService()
        self.MetricsDatasetService = MetricsDatasetService()
        self.MetricsService = MetricsService()

    @staticmethod
    def generate_kpi_from_template(title, metric, dates, values, footer, label):
        result = dict()
        if title:
            result["title"] = title
        if metric:
            result["metric"] = f"{intcomma(f'{metric: .02f}')} BYN"
        if footer:
            if footer >= 0:
                color_class = "text-green-700 font-semibold dark:text-green-400"
                sign = "+"
            else:
                color_class = "text-red-700 font-semibold dark:text-red-400"
                sign = "-"

            formatted_footer = f'<strong class="{color_class}">{sign}{intcomma(f"{footer:.02f}")}%</strong>&nbsp; по сравнению с предыдущим периудом'

            result["footer"] = mark_safe(formatted_footer)
        if dates and values:
            result["chart"] = json.dumps(
                {
                    "labels": dates,
                    "datasets": [{"data": values, "borderColor": "#9333ea"}],
                }
            )
        if label:
            result["label"] = label

        return result

    @staticmethod
    def generate_progress_from_template(dataset):
        all_progress = []

        for item in dataset:
            all_progress.append(
                {
                    "title": item["title"],
                    "description": str(
                        intcomma(f"{item['description']: .02f}") + " BYN"
                    ),
                    "value": item["value"],
                }
            )

        return all_progress

    def generate_kpi(self):
        all_kpi = []

        total_revenue_week = self.generate_kpi_from_template(
            "Выручка",
            self.MetricsTotalService.get_total_revenue_by_week(),
            *self.MetricsDatasetService.get_weekly_revenue(),
            self.MetricsTotalService.get_total_revenue_growth_by_week(),
            label="Текущая неделя",
        )

        total_revenue_month = self.generate_kpi_from_template(
            "Выручка",
            self.MetricsTotalService.get_total_revenue_by_month(),
            *self.MetricsDatasetService.get_monthly_revenue(),
            self.MetricsTotalService.get_total_revenue_growth_by_month(),
            label="Текущий месяц",
        )

        all_kpi.append(total_revenue_week)
        all_kpi.append(total_revenue_month)

        return all_kpi

    def generate_performance(self):
        all_performance = []

        total_revenue_quarter = self.generate_kpi_from_template(
            "Выручка",
            self.MetricsTotalService.get_total_revenue_by_quarter(),
            *self.MetricsDatasetService.get_quarterly_revenue(),
            self.MetricsTotalService.get_total_revenue_growth_by_quarter(),
            label="Текущий квартал",
        )

        total_revenue_year = self.generate_kpi_from_template(
            "Выручка",
            self.MetricsTotalService.get_total_revenue_by_year(),
            *self.MetricsDatasetService.get_yearly_revenue(),
            self.MetricsTotalService.get_total_revenue_growth_by_year(),
            label="Текущий год",
        )

        all_performance.append(total_revenue_quarter)
        all_performance.append(total_revenue_year)

        return all_performance

    def generate_progress_week(self):
        return self.generate_progress_from_template(
            self.MetricsService.get_revenue_share_by_product_for_week()
        )

    def generate_progress_month(self):
        return self.generate_progress_from_template(
            self.MetricsService.get_revenue_share_by_product_for_month()
        )


class OrderService:
    @classmethod
    def get_orders_by_period(cls, start: datetime, end: datetime):
        """Получает заказы за указанный период с предзагрузкой связанных объектов."""
        return Order.objects.prefetch_related("items", "items__product").filter(
            created_at__date__range=(start, end)
        )


class MetricsService:
    WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    MONTH_NAMES = [
        "Янв",
        "Фев",
        "Мар",
        "Апр",
        "Май",
        "Июн",
        "Июл",
        "Авг",
        "Сен",
        "Окт",
        "Ноя",
        "Дек",
    ]

    @staticmethod
    def get_orders_by_period(start: datetime, end: datetime):
        return OrderService.get_orders_by_period(start, end)

    @staticmethod
    def aggregate_total_revenue(orders: QuerySet):
        return (
            orders.annotate(
                item_total_price=F("items__quantity") * F("items__product__price")
            ).aggregate(total_revenue=Sum("item_total_price"))["total_revenue"]
            or 0.0
        )

    def get_total_revenue_by_period(
        self, start: datetime, end: datetime, cache_key=str
    ) -> float:
        orders = self.get_orders_by_period(start, end)
        return float(self.aggregate_total_revenue(orders))

    def get_revenue_share_by_product(self, start: datetime, end: datetime):
        """Возвращает долю дохода по каждому продукту за указанный период."""
        orders = self.get_orders_by_period(start, end)

        # Группируем по продукту (по ID) и считаем сумму выручки для каждого товара

        product_revenue = (
            orders.values(
                "items__product__id", "items__product__name"
            )  # Группировка только по этим полям
            .annotate(
                revenue=Sum(F("items__quantity") * F("items__product__price"))
            )  # Суммирование
            .order_by(
                "items__product__id"
            )  # Упорядочивание по ID продукта (необязательно)
        )

        total_revenue = sum(item["revenue"] for item in product_revenue)

        return [
            {
                "title": item["items__product__name"],
                "description": item["revenue"],
                "value": (
                    int(item["revenue"] / total_revenue * 100) if total_revenue else 0
                ),
            }
            for item in product_revenue
        ]

    def get_revenue_share_by_product_for_week(self):
        start, end = DateTimeService.current_week()
        return self.get_revenue_share_by_product(start, end)

    def get_revenue_share_by_product_for_month(self):
        start, end = DateTimeService.current_month()
        return self.get_revenue_share_by_product(start, end)


class MetricsTotalService(MetricsService):

    def get_total_revenue_by_period_and_aggregate(
        self, period_func: Callable, cache_key: str
    ):
        start, end = period_func()
        if cache_key in redis_cache:
            products = redis_cache.get(cache_key)
        else:
            products = self.get_total_revenue_by_period(start, end)
            redis_cache.set(
                cache_key, products, timeout=METRICS_CACHE_TIMEOUTS[cache_key]
            )
        return products

    def get_total_revenue_growth(
        self, current_func: Callable, previous_func: Callable, cache_key: str
    ):
        if cache_key in redis_cache:
            return redis_cache.get(cache_key)
        else:
            current_start, current_end = current_func()
            previous_start, previous_end = previous_func()

            current_revenue = self.get_total_revenue_by_period(
                current_start, current_end
            )
            previous_revenue = self.get_total_revenue_by_period(
                previous_start, previous_end
            )

            if previous_revenue == 0:
                return float("inf") if current_revenue > 0 else 0.0

            result = ((current_revenue - previous_revenue) / previous_revenue) * 100

            redis_cache.set(
                cache_key, result, timeout=METRICS_CACHE_TIMEOUTS[cache_key]
            )

            return result

    def get_total_revenue_by_week(self):
        return self.get_total_revenue_by_period_and_aggregate(
            DateTimeService.current_week, cache_key="total_revenue_by_week"
        )

    def get_total_revenue_by_month(self):
        return self.get_total_revenue_by_period_and_aggregate(
            DateTimeService.current_month, cache_key="total_revenue_by_month"
        )

    def get_total_revenue_by_quarter(self):
        return self.get_total_revenue_by_period_and_aggregate(
            DateTimeService.current_quarter, cache_key="total_revenue_by_quarter"
        )

    def get_total_revenue_by_year(self):
        return self.get_total_revenue_by_period_and_aggregate(
            DateTimeService.current_year, cache_key="total_revenue_by_year"
        )

    def get_total_revenue_growth_by_week(self):
        return self.get_total_revenue_growth(
            DateTimeService.current_week,
            DateTimeService.previous_week,
            cache_key="total_revenue_growth_by_week",
        )

    def get_total_revenue_growth_by_month(self):
        return self.get_total_revenue_growth(
            DateTimeService.current_month,
            DateTimeService.previous_month,
            cache_key="total_revenue_growth_by_month",
        )

    def get_total_revenue_growth_by_quarter(self):
        return self.get_total_revenue_growth(
            DateTimeService.current_quarter,
            DateTimeService.previous_quarter,
            cache_key="total_revenue_growth_by_quarter",
        )

    def get_total_revenue_growth_by_year(self):
        return self.get_total_revenue_growth(
            DateTimeService.current_year,
            DateTimeService.previous_year,
            cache_key="total_revenue_growth_by_year",
        )

    def get_total_orders_by_period(self, period_func: Callable, cache_key: str):
        start, end = period_func()
        if cache_key in redis_cache:
            result = redis_cache.get(cache_key)
        else:
            result = self.get_orders_by_period(start, end).count()
            redis_cache.set(
                cache_key, result, timeout=METRICS_CACHE_TIMEOUTS[cache_key]
            )
        return result

    def get_total_orders_by_week(self):
        return self.get_total_orders_by_period(
            DateTimeService.current_week, cache_key="total_orders_by_week"
        )

    def get_total_orders_by_month(self):
        return self.get_total_orders_by_period(
            DateTimeService.current_month, cache_key="total_orders_by_month"
        )


class MetricsAverageService(MetricsService):
    def get_average_order_value_by_period(
        self, start: datetime, end: datetime
    ) -> float:
        """
        Возвращает среднюю стоимость заказа за указанный период.
        """
        orders = self.get_orders_by_period(start, end)
        aggregated = orders.aggregate(
            total_revenue=Sum(F("items__quantity") * F("items__product__price")),
            total_orders=Count("id"),
        )
        total_revenue = aggregated["total_revenue"] or 0
        total_orders = aggregated["total_orders"] or 0

        return total_revenue / total_orders if total_orders else 0.0

    def get_average_order_value_by_week(self) -> float:
        """
        Возвращает среднюю стоимость заказа за текущую неделю.
        """
        start, end = DateTimeService.current_week()
        return self.get_average_order_value_by_period(start, end)

    def get_average_order_value_by_month(self) -> float:
        """
        Возвращает среднюю стоимость заказа за текущий месяц.
        """
        start, end = DateTimeService.current_month()
        return self.get_average_order_value_by_period(start, end)


class MetricsDatasetService(MetricsService):

    def get_weekly_revenue(self):
        """
        Возвращает два массива: дни недели и значения прибыли по дням недели.
        """
        start, end = DateTimeService.current_week()
        dates, values = [], []
        current = start
        cache_key = "weekly_revenue"
        if cache_key in redis_cache:
            return redis_cache.get(cache_key)
        else:
            while current <= end:
                day_start = current
                day_end = current - timedelta(seconds=1)
                revenue = self.get_total_revenue_by_period(day_start, day_end)
                dates.append(self.WEEKDAYS[current.weekday()])
                values.append(revenue)
                current += timedelta(days=1)
                redis_cache.set(
                    cache_key,
                    (dates, values),
                    timeout=METRICS_CACHE_TIMEOUTS[cache_key],
                )
            return dates, values

    def get_monthly_revenue(self):
        """
        Возвращает два массива: дни месяца и значения прибыли по дням текущего месяца.
        """
        start, end = DateTimeService.current_month()
        dates, values = [], []
        current = start
        cache_key = "monthly_revenue"
        if cache_key in redis_cache:
            return redis_cache.get(cache_key)
        else:
            while current <= end:
                day_start = current
                day_end = current - timedelta(seconds=1)
                revenue = self.get_total_revenue_by_period(day_start, day_end)
                dates.append(current.day)
                values.append(revenue)
                current += timedelta(days=1)
                redis_cache.set(
                    cache_key,
                    (dates, values),
                    timeout=METRICS_CACHE_TIMEOUTS[cache_key],
                )
            return dates, values

    def get_quarterly_revenue(self):
        """
        Возвращает два массива: месяцы текущего квартала и значения прибыли по каждому месяцу квартала.
        """
        start, end = DateTimeService.current_quarter()
        current = start
        dates, values = [], []
        cache_key = "quarterly_revenue"
        if cache_key in redis_cache:
            return redis_cache.get(cache_key)
        else:
            while current <= end:
                month_start = current
                _, days_in_month = monthrange(current.year, current.month)
                month_end = month_start + timedelta(days=days_in_month - 1)
                revenue = self.get_total_revenue_by_period(month_start, month_end)
                dates.append(self.MONTH_NAMES[current.month - 1])
                values.append(revenue)
                current += timedelta(days=days_in_month)
                redis_cache.set(
                    cache_key,
                    (dates, values),
                    timeout=METRICS_CACHE_TIMEOUTS[cache_key],
                )
            return dates, values

    def get_yearly_revenue(self):
        """
        Возвращает два массива: названия месяцев текущего года и значения прибыли по каждому месяцу.
        """
        start, end = DateTimeService.current_year()
        dates, values = [], []
        current = start
        cache_key = "yearly_revenue"
        if cache_key in redis_cache:
            return redis_cache.get(cache_key)
        else:
            while current <= end:
                month_start = current.replace(day=1)
                _, days_in_month = monthrange(current.year, current.month)
                month_end = month_start + timedelta(days=days_in_month - 1)

                revenue = self.get_total_revenue_by_period(month_start, month_end)
                # Читаемое имя месяца
                dates.append(self.MONTH_NAMES[month_start.month - 1])
                values.append(revenue)

                current = month_start + timedelta(days=days_in_month)
                redis_cache.set(
                    cache_key,
                    (dates, values),
                    timeout=METRICS_CACHE_TIMEOUTS[cache_key],
                )
            return dates, values
