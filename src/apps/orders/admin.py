from typing import Union

from apps.orders.views import DeliveryMapView
from apps.orders.views import DeliveryView
from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_catalog.settings import env_config
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from unfold.contrib.filters.admin import FieldTextFilter
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.contrib.filters.admin import RelatedDropdownFilter
from unfold.decorators import action
from unfold.decorators import display

from .models import Cart
from .models import CartItem
from .models import Delivery
from .models import Order
from .models import OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    tab = True

    readonly_fields = [
        "total_price",
    ]


class OrderInline(TabularInline):
    model = Order
    extra = 0
    tab = True
    can_delete = False
    fields = (
        "customer_first_name",
        "customer_last_name",
        "customer_phone",
        "payment_method",
        "delivery_address",
        "status",
    )

    readonly_fields = (
        "customer_first_name",
        "customer_last_name",
        "customer_phone",
        "payment_method",
        "delivery_address",
        "status",
    )


@admin.register(Delivery)
class DeliveryAdmin(ModelAdmin):
    list_editable = ("status",)
    list_filter = (
        ("status", ChoicesDropdownFilter),
        ("created_at", RangeDateFilter),
    )
    readonly_fields = ("created_at", "total_distance")

    list_display = ("courier", "status", "created_at", "shop_address", "total_distance")

    inlines = [
        OrderInline,
    ]

    actions_detail = ["create_map"]
    ordering = ["-created_at"]

    def get_urls(self):
        return super().get_urls() + [
            path(
                "map/<int:object_id>",
                DeliveryMapView.as_view(model_admin=self),
                name="delivery-map",
            ),
        ]

    @action(description="Построить карту")
    def create_map(self, request, object_id: int):
        return redirect(reverse_lazy("admin:delivery-map", args=(object_id,)))


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [OrderItemInline]

    search_fields = (
        "customer_first_name",
        "customer_last_name",
        "customer_email",
        "customer_phone",
    )
    list_editable = ("status",)
    list_filter = (
        ("customer_email", FieldTextFilter),
        ("customer_phone", FieldTextFilter),
        ("payment_method", ChoicesDropdownFilter),
        ("delivery_method", ChoicesDropdownFilter),
        ("delivery_address", ChoicesDropdownFilter),
        ("pickup_address", RelatedDropdownFilter),
        ("status", ChoicesDropdownFilter),
        ("created_at", RangeDateTimeFilter),
    )
    readonly_fields = (
        "created_at",
        "session_id",
        "total_price",
    )

    list_display = (
        "display_header",
        "customer_email",
        "status",
        "created_at",
        "total_price",
    )

    ordering = ["-created_at"]

    warn_unsaved_form = True if env_config.ENVIROMENT == "production" else False

    list_filter_sheet = False
    list_filter_submit = True

    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    (
                        "customer_first_name",
                        "customer_last_name",
                    ),
                    (
                        "customer_email",
                        "customer_phone",
                    ),
                )
            },
        ),
        (
            _("Order info"),
            {
                "fields": (
                    (
                        "status",
                        "created_at",
                        "total_price",
                    ),
                    "payment_method",
                    "delivery_method",
                    "delivery_address",
                    "pickup_address",
                )
            },
        ),
    )

    @display(description=_("Заказ"), header=True)
    def display_header(self, instance: Cart):
        return [instance.customer_first_name, instance.customer_phone]

    def total_price(self, obj):
        return obj.total_price

    actions = ["select_orders_for_assignment"]

    def get_urls(self):
        return super().get_urls() + [
            path(
                "assign_courier",
                DeliveryView.as_view(model_admin=self),
                name="assign_courier",
            ),
        ]

    @action(description="Назначить курьера для выбранных заказов")
    def select_orders_for_assignment(self, request, queryset):
        # Сохраняем выбранные заказы в сессии
        request.session["selected_orders"] = list(queryset.values_list("id", flat=True))
        return redirect("admin:assign_courier")


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    tab = True


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    inlines = [CartItemInline]
