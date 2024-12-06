import logging
import random
from typing import Union

import folium
import networkx as nx
import osmnx as ox
from apps.main.models import Address
from apps.main.models import Category
from apps.main.models import Phone
from apps.utills import get_address_from_coordinates
from apps.utills import reorder_coordinates
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django_catalog.settings import env_config
from drf_spectacular.utils import extend_schema
from folium import plugins
from openrouteservice import Client
from openrouteservice import distance_matrix
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from unfold.views import UnfoldModelAdminViewMixin

from .forms import OrderForm
from .models import Cart
from .models import CartItem
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
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
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
                request, "empty_cart.html", {"message": "Ваша корзина пуста."}
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
                        "product",
                        "К сожалению один из товаров поставляется только под заказ. Пожалуйста оставьте заявку через форму обратной связи",
                    )
                    content["form"] = form
                    return render(request, "main/checkout.html", content)
                order.items.create(product=item.product, quantity=item.quantity)

            # Очищаем корзину
            cart.items.all().delete()

            # Рендерим страницу с подтверждением заказа
            return redirect("catalog")
        else:
            return render(request, "main/checkout.html", content)


class DeliveryView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Выбор маршрута"
    permission_required = ()
    template_name = "admin/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client = Client(key=env_config.OPEN_ROUTE_SERVICE_API_KEY)

        orders = Order.objects.filter(
            Q(longitude__isnull=False) & Q(latitude__isnull=False)
        )

        # Список всех точек
        ors_coordinates = [(order.longitude, order.latitude) for order in orders]

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

        # Простейший алгоритм для решения TSP
        # Находим оптимальный порядок посещения точек
        from itertools import permutations

        def calculate_route_order(distances):
            n = len(distances)
            # Генерируем все маршруты, начиная с точки 0
            all_routes = permutations(range(1, n))
            min_distance = float("inf")
            best_route = []
            for route in all_routes:
                # Начальная точка до первой в маршруте
                current_distance = distances[0][route[0]]
                for i in range(len(route) - 1):
                    current_distance += distances[route[i]][route[i + 1]]
                # Возврат в начальную точку
                current_distance += distances[route[-1]][0]
                if current_distance < min_distance:
                    min_distance = current_distance
                    best_route = [0] + list(route) + [0]
            return best_route, min_distance

        # Получаем оптимальный порядок маршрута
        route_order, total_distance = calculate_route_order(matrix["distances"])

        # Переставляем координаты в соответствии с маршрутом
        optimal_route = [ors_coordinates[i] for i in route_order]

        # Запрашиваем маршрут для оптимального порядка точек
        route_geojson = client.directions(
            coordinates=optimal_route, profile="driving-car", format="geojson"
        )

        # Отображаем карту с оптимальным маршрутом
        m = folium.Map(location=reorder_coordinates(ors_coordinates[0]), zoom_start=14)

        # Добавляем точки на карту
        for i, coord in enumerate(optimal_route):
            popup_text = get_address_from_coordinates(orders, coord)
            if i == 0 or i == len(optimal_route) - 1:
                folium.CircleMarker(
                    location=(coord[1], coord[0]),
                    radius=15,
                    color="red",
                    fill=True,
                    fill_color="red",
                    popup="Магазин",
                ).add_to(m)
            else:
                folium.Marker(
                    location=(coord[1], coord[0]), popup=f"{i}. {popup_text}"
                ).add_to(m)

        # Добавляем маршрут на карту с уникальным цветом
        for i, feature in enumerate(route_geojson["features"]):
            route_coords = feature["geometry"]["coordinates"]

            folium.PolyLine(
                locations=[
                    (lat, lon) for lon, lat in route_coords
                ],  # Порядок: (lat, lon)
                color="blue",  # Цвет маршрута
                weight=4,  # Толщина линии
                opacity=0.7,  # Прозрачность линии
            ).add_to(m)

        plugins.Fullscreen().add_to(m)

        # Сохранение карты в HTML
        map_html = m._repr_html_()

        # Сохранение карты
        context["map_html"] = map_html
        return context
