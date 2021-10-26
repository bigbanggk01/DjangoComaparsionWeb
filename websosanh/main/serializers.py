from django.db import models
from rest_framework import serializers
from .models import product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['id','name','url','price','image_link','description','brand']