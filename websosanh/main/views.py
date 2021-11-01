from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import product
from .serializers import ProductSerializer
from rest_framework import generics

class GetAllProductAPIView(generics.ListCreateAPIView):
    queryset = product.objects.all()
    serializer_class = ProductSerializer