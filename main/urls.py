from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('catalog', catalog, name='catalog'),
    path('product/<str:slug>/', currentProduct, name='current-product'),
    path('catalog/<str:slug>', currentCategory, name='current-category'),
    path('catalog/<str:slug>/collections', currentCategory, name='collections'),
    path('catalog/collections/<str:slug>', currentCategory, name='current-collection'),
]