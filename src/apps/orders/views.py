from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart
from .models import CartItem
from .models import Order
from .models import Product
from .serializers import CartItemSerializer
from .serializers import CartSerializer
from .serializers import OrderSerializer
from .utils import get_cart


class CartView(APIView):
    def get(self, request):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartView(APIView):
    def post(self, request, product_id):
        cart = get_cart(request)
        product = Product.objects.get(id=product_id)
        quantity = int(request.data.get("quantity", 1))

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return Response(
            {"message": "Product added to cart"}, status=status.HTTP_201_CREATED
        )


class RemoveFromCartView(APIView):
    def post(self, request, product_id):
        cart = get_cart(request)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response(
            {"message": "Product removed from cart"}, status=status.HTTP_200_OK
        )


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CreateOrderView(CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        cart = get_cart(self.request)
        order = serializer.save(session_id=cart.session_id)
        for item in cart.items.select_related("product").all():
            order.items.create(product=item.product, quantity=item.quantity)
        cart.items.all().delete()
