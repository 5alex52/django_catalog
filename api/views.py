from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.models import Feedback, Product, ProductImage
from .serializers import FeedbackSerializer, ProductSerializer, ImageSerializer
from django.utils import timezone
import os
from dotenv import load_dotenv
load_dotenv()


class FeedbackListApiView(APIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('date') and request.GET.get('token') == str(os.getenv('API_TOKEN')):
            feedback_list = Feedback.objects.all().exclude(date__lte=request.GET.get('date'))
            serializer = FeedbackSerializer(feedback_list, many=True)
            return Response({'users': serializer.data, 'date':timezone.now()}, status=status.HTTP_200_OK)
        else:
            return Response({'loser': 'you'}, status=status.HTTP_400_BAD_REQUEST)
        
class ProductListApiView(APIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('date') and request.GET.get('token') == str(os.getenv('API_TOKEN')):
            products = Product.objects.all().exclude(date__lte=request.GET.get('date'))
            serializer = ProductSerializer(products, many=True, context={"request":request})
            return Response({'products': serializer.data, 'date':timezone.now()}, status=status.HTTP_200_OK)
        else:
            return Response({'loser': 'you'}, status=status.HTTP_400_BAD_REQUEST)
        

class ImageListApiView(APIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        product = Product.objects.get(slug=slug)
        images= ProductImage.objects.filter(product=product)
        serializer = ImageSerializer(images, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)