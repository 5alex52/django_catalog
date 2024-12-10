import logging

from apps.main.models import Address
from apps.main.models import Category
from apps.main.models import Phone
from apps.orders.services import DeliveryService
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django_catalog.settings import env_config
from drf_spectacular.utils import extend_schema
from openrouteservice import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from unfold.views import UnfoldModelAdminViewMixin

from .forms import AssignCourierForm
from .forms import OrderForm
from .models import Cart
from .models import CartItem
from .models import Delivery
from .models import Order
from .models import Product
from .serializers import CartSerializer
from .utils import get_cart

logger = logging.getLogger()


@extend_schema(tags=["Cart"])
class CartViewSet(ViewSet):
    """
    A ViewSet for managing the shopping cart.
    """

    def list(self, request):
        """
        Retrieve the current cart and its items.
        """
        cart = get_cart(request)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)

    def add(self, request, product_id=None):
        """
        Add a product to the cart.
        """
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

    def remove(self, request, product_id=None):
        """
        Remove a product from the cart.
        """
        cart = get_cart(request)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product_id
        )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return Response(
            {"message": "Product removed from cart"}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Order"])
class OrderCreateView(View):
    """
    View для отображения формы создания заказа, обработки данных формы и создания заказа.
    """

    def get(self, request, *args, **kwargs):
        """
        Отображение формы создания заказа.
        """
        phones = Phone.objects.all().select_related("store")
        address = Address.objects.order_by("pk")
        categories = Category.objects.order_by("number")

        cart = get_cart(request)

        if not cart.items.exists():
            return render(
                request, "main/checkout.html", {"message": "Ваша корзина пуста."}
            )

        form = OrderForm()

        content = {
            "cart": cart,
            "phones": phones,
            "categories": categories,
            "address": address,
            "form": form,
        }

        return render(request, "main/checkout.html", content)

    def post(self, request, *args, **kwargs):
        """
        Обработка данных формы и создание заказа.
        """
        cart: Cart = get_cart(request)
        form = OrderForm(request.POST)

        phones = Phone.objects.all().select_related("store")
        address = Address.objects.order_by("pk")
        categories = Category.objects.order_by("number")

        content = {
            "cart": cart,
            "phones": phones,
            "categories": categories,
            "address": address,
            "form": form,
        }

        if form.is_valid():
            # Создаем заказ
            order = form.save(commit=False)
            order.session_id = cart.session_id
            order.save()

            # Переносим товары из корзины в заказ
            for item in cart.items.select_related("product").all():
                if item.product.price == 0:
                    form.add_error(
                        None,
                        "К сожалению один из товаров поставляется только под заказ. Пожалуйста оставьте заявку через форму обратной связи",
                    )
                    order.delete()
                    content["form"] = form
                    return render(request, "main/checkout.html", content)
                order.items.create(product=item.product, quantity=item.quantity)

            # Очищаем корзину
            cart.items.all().delete()

            # Рендерим страницу с подтверждением заказа
            return redirect("catalog")
        else:
            return render(request, "main/checkout.html", content)


class DeliveryMapView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Выбор маршрута"
    permission_required = ()
    template_name = "admin/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        delivery_id = kwargs.pop("object_id", None)

        client = Client(key=env_config.OPEN_ROUTE_SERVICE_API_KEY)

        delivery = Delivery.objects.get(id=delivery_id)

        orders = delivery.orders.all()

        ors_coordinates = [
            (delivery.shop_address.longitude, delivery.shop_address.latitude)
        ]

        ors_coordinates.extend([(order.longitude, order.latitude) for order in orders])

        # Рассчитываем матрицу расстояний
        matrix = client.distance_matrix(
            locations=ors_coordinates,  # Список координат
            profile="driving-car",  # Тип транспорта
            metrics=[
                "distance"
            ],  # Метрика: расстояние (можно добавить 'duration', если нужен расчет времени)
            units="m",  # Единицы измерения: метры
            validate=True,
        )

        # Получаем оптимальный порядок маршрута
        route_order, total_distance = DeliveryService.calculate_route_order(
            matrix["distances"]
        )

        # Переставляем координаты в соответствии с маршрутом
        optimal_route = [ors_coordinates[i] for i in route_order]

        # Запрашиваем маршрут для оптимального порядка точек
        route_geojson = client.directions(
            coordinates=optimal_route, profile="driving-car", format="geojson"
        )
        delivery.total_distance = round(total_distance / 1000, 2)
        delivery.status = "In progress"
        delivery.save()

        context["map_html"] = DeliveryService.create_route_map(
            ors_coordinates, optimal_route, orders, route_geojson
        )
        return context


class DeliveryView(UnfoldModelAdminViewMixin, FormView):
    title = "Выбор товаров для доставки"
    form_class = AssignCourierForm
    success_url = reverse_lazy("admin:orders_order_changelist")
    template_name = "admin/delivery.html"
    permission_required = ()

    def form_valid(self, form):
        delivery = form.cleaned_data["delivery"]
        order_ids = self.request.session.get("selected_orders", [])
        orders = Order.objects.filter(id__in=order_ids, delivery_method="Delivery")
        assigned_count = 0

        for order in orders:
            order.delivery = delivery
            order.status = "In progress"
            order.save()
            assigned_count += 1
        if assigned_count == 0:
            messages.error(
                self.request, "Ни один из заказов не подходит для назначения доставки"
            )
        else:
            messages.success(
                self.request,
                f"Успешно назначено {assigned_count} заказов курьеру {delivery.courier} на {delivery.created_at}",
            )
        if assigned_count != len(order_ids):
            messages.warning(
                self.request,
                "Не все заказы подходят для доставки. Проверьте метод доставки",
            )
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.session.get("selected_orders"):
            messages.error(request, "Вы не выбрали заказы для назначения.")
            return redirect("admin:orders_order_changelist")
        return super().get(request, *args, **kwargs)
