from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from main.models import Feedback
from .serializers import FeedbackSerializer
from django.utils import timezone
from datetime import timedelta


class FeedbackListApiView(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    # http://127.0.0.1:8000/feedback/api?date=2023-04-29T11:18:06.023938Z
    def get(self, request, *args, **kwargs):
        if request.GET.get('date'):
            feedback_list = Feedback.objects.all().exclude(date__lte=request.GET.get('date'))
            serializer = FeedbackSerializer(feedback_list, many=True)
            return Response({'users': serializer.data, 'date':timezone.now()}, status=status.HTTP_200_OK)
        else:
            feedback_list = Feedback.objects.all()
            serializer = FeedbackSerializer(feedback_list, many=True)
            return Response({'users': serializer.data, 'date':timezone.now()}, status=status.HTTP_200_OK)
