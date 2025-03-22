import datetime
import random
import uuid
from unittest.mock import MagicMock
from unittest.mock import patch

import factory
import pytest
from apps.main.models import Address
from apps.main.models import Category
from apps.main.models import Collection
from apps.main.models import Feedback
from apps.main.models import Manufacturer
from apps.main.models import Phone
from apps.main.models import Product
from apps.main.models import Specs
from apps.orders.models import Cart
from apps.orders.models import Delivery
from apps.orders.models import Order
from apps.orders.models import OrderItem
from apps.orders.services import MetricsService
from apps.orders.services import MetricsTotalService
from apps.orders.services import MetricsVisualService
from django.test import Client
from django.utils import timezone
from faker import Faker
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_product(db):
    return Product.objects.create(name="Test Product", price=100, isOnSale=False)


@pytest.fixture
def mock_get_cart():
    with patch("apps.orders.views.get_cart") as mock:
        mock.return_value = Cart(session_id="test_session_id", id=1)
        yield mock


@pytest.fixture
def metrics_visual_service() -> MetricsVisualService:
    return MetricsVisualService()


@pytest.fixture
def mock_now():
    with patch("apps.orders.services.now") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_redis():
    with patch("django_redis.get_redis_connection") as mock:
        mock.return_value = MagicMock()
        yield mock


@pytest.fixture
def metrics_total_service():
    return MetricsTotalService()


@pytest.fixture
def metrics_service():
    return MetricsService()


fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    slug = factory.Faker("slug")
    number = factory.Sequence(lambda n: n + 1)
    isCabinet = factory.Faker("boolean")


class ManufacturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manufacturer

    name = factory.Faker("company")
    slug = factory.Faker("slug")


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    name = factory.Faker("word")
    manufacturer = factory.SubFactory(ManufacturerFactory)
    image = factory.django.ImageField()
    slug = factory.Faker("slug")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    manufacturer = factory.SubFactory(ManufacturerFactory)
    category = factory.SubFactory(CategoryFactory)
    collection = factory.SubFactory(CollectionFactory)
    isOnSale = factory.Faker("boolean")
    rating = factory.LazyFunction(lambda: random.randint(1, 1000))
    mainImage = factory.django.ImageField()
    slug = factory.Faker("slug")
    date = factory.LazyFunction(timezone.now)
    price = factory.Faker("random_number", digits=4)

    @factory.post_generation
    def collectionCategory(self, create, extracted, **kwargs):
        if extracted:
            for category in extracted:
                self.collectionCategory.add(category)


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    session_id = factory.LazyFunction(lambda: uuid.uuid4())
    created_at = factory.LazyFunction(lambda: datetime.datetime.today())
    updated_at = factory.LazyFunction(lambda: datetime.datetime.today())


class SpecsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Specs

    product = factory.SubFactory(ProductFactory)
    param = factory.Faker("word")
    value = factory.Faker("word")
    unit = factory.Faker("word")


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    name = factory.Faker("company")
    street = factory.Faker("street_name")
    number = factory.Faker("building_number")
    building = factory.Faker("word")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")


class PhoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Phone

    phone = factory.Faker("phone_number")
    isViber = factory.Faker("boolean")
    store = factory.SubFactory(AddressFactory)


class FeedbackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feedback

    name = factory.Faker("name")
    phone = factory.Faker("phone_number")
    product = factory.SubFactory(ProductFactory)
    product_name = factory.Faker("word")
    date = factory.LazyFunction(timezone.now)
    link = factory.Faker("url")


class DeliveryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Delivery

    method = factory.Faker("word")


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer_first_name = factory.Faker("first_name")
    customer_last_name = factory.Faker("last_name")
    customer_email = factory.Faker("email")
    customer_phone = factory.Faker("phone_number")
    payment_method = "Card"  # Пример
    delivery_method = "Courier"  # Пример
    delivery_address = factory.Faker("address")
    status = "New"
    latitude = None
    longitude = None
    created_at = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if extracted:
            for item in extracted:
                self.items.add(item)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=5)
