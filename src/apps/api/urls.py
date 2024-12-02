from django.urls import path
from .views import FeedbackListApiView, ProductListApiView, ImageListApiView

urlpatterns = [
    path("feedback/", FeedbackListApiView.as_view()),
    path("product/", ProductListApiView.as_view()),
    path("product/<str:slug>/", ImageListApiView.as_view()),
]
