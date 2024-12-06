from django.urls import path

from .views import catalog
from .views import CollectionAutocomplete
from .views import collections
from .views import contacts
from .views import currentCategory
from .views import currentCollection
from .views import currentCollectionFromCategory
from .views import currentManufacturer
from .views import currentProduct
from .views import home
from .views import sales
from .views import searchHendler


urlpatterns = [
    path("", home, name="home"),
    path("catalog/", catalog, name="catalog"),
    path("product/<str:slug>/", currentProduct, name="current-product"),
    path("catalog/<str:slug>/", currentCategory, name="current-category"),
    path("catalog/<str:slug>/collections/", collections, name="current-collections"),
    path(
        "catalog/<str:slug>/collections/<str:slug2>/",
        currentCollectionFromCategory,
        name="collections-category",
    ),
    path("collections/<str:slug>/", currentCollection, name="current-collection"),
    path("sales/", sales, name="sales"),
    path("contacts/", contacts, name="contacts"),
    path("search/", searchHendler, name="search"),
    path("manufacturer/<str:slug>/", currentManufacturer, name="current-manufacturer"),
    path(
        "collection-autocomplete/",
        CollectionAutocomplete.as_view(),
        name="collection-autocomplete",
    ),
]
