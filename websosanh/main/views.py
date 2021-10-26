from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import product
from .serializers import ProductSerializer

class GetAllProductAPIView(APIView):
    def get(self, request):
        list_product = product.objects.all()
        data = ProductSerializer(list_product, many=True)
        return Response(data=data.data, status = status.HTTP_200_OK)