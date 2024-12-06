from django.urls import path

from .views import AddToCartView
from .views import CartView
from .views import CreateOrderView
from .views import OrderDetailView
from .views import OrderListView
from .views import RemoveFromCartView


urlpatterns = [
    # Корзина
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path(
        "cart/remove/<int:product_id>/",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    # Заказы
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/create/", CreateOrderView.as_view(), name="create_order"),
]
