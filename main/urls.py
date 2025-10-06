from django.urls import path

from .views import *


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
