from rest_framework import serializers

from .models import Cart
from .models import CartItem
from .models import Order
from .models import OrderItem


# Сериализатор для товара в корзине
class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


# Сериализатор для корзины
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "session_id", "created_at", "updated_at", "items"]


# Сериализатор для позиции заказа
class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "total_price"]


# Сериализатор для заказа
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "session_id",
            "created_at",
            "customer_first_name",
            "customer_last_name",
            "customer_email",
            "customer_phone",
            "payment_method",
            "delivery_method",
            "delivery_address",
            "pickup_address",
            "status",
            "items",
        ]
