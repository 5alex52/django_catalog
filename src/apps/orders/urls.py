from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CartViewSet
from .views import OrderCreateView

router = DefaultRouter()
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
    path("checkout/", OrderCreateView.as_view(), name="checkout"),
    path(
        "cart/add/<int:product_id>/",
        CartViewSet.as_view({"post": "add"}),
        name="cart-add",
    ),
    path(
        "cart/remove/<int:product_id>/",
        CartViewSet.as_view({"post": "remove"}),
        name="cart-remove",
    ),
]
