from django.urls import path
from .views import FeedbackListApiView

urlpatterns = [
    path('api', FeedbackListApiView.as_view()),
]