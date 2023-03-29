from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('product/<str:slug>/', currentProduct, name='current-product'),
    path('catalog/<str:slug>', currentCategory, name='current-category'),
    path('catalog/<str:slug>/collections/', collections, name='current-collections'),
    path('collections/<str:slug>/', currentCollection, name='current-collection'),
    path('sales/', sales, name='sales'),
    path('contacts', contacts, name='contacts'),
    path('manufacturer/<str:slug>/', currentManufacturer, name='current-manufacturer'),
]