from django.urls import path

from .views import FeedbackListApiView
from .views import ImageListApiView
from .views import ProductListApiView

urlpatterns = [
    path("feedback/", FeedbackListApiView.as_view()),
    path("product/", ProductListApiView.as_view()),
    path("product/<str:slug>/", ImageListApiView.as_view()),
]
