from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_catalog.settings import env_config
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline
from unfold.admin import TabularInline
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from unfold.contrib.filters.admin import FieldTextFilter
from unfold.contrib.filters.admin import RangeDateFilter
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.contrib.filters.admin import RelatedDropdownFilter
from unfold.decorators import display

from .models import Cart
from .models import CartItem
from .models import Order
from .models import OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    tab = True

    readonly_fields = [
        "total_price",
    ]


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


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    tab = True


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    inlines = [CartItemInline]
