from django.db.models import query
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import product
from .serializers import ProductSerializer
from rest_framework import generics
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

PRODUCT_PER_PAGE = 60
def home(request):
    q = request.GET.get('q')
    if q is not None:
        return redirect('/main/?q='+q)
    else:
        return render(request,'main/home.html')   

def index(request):
    context = {}
    query = ""
    if request.GET:
        query = request.GET.get('q','')
        context['query'] = str(query)

    products = product.objects.filter(name__search=query).all()
    context['products'] = products

    #pagination
    page = request.GET.get('page',1)
    products_paginator = Paginator(products, PRODUCT_PER_PAGE)
    
    try:
        products = products_paginator.page(page)
    except PageNotAnInteger:
        products = products_paginator.page(PRODUCT_PER_PAGE)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)

    context['products'] = products
    return render(request, 'main/product.html', context)

class GetAllProductAPIView(generics.ListCreateAPIView):
    queryset = product.objects.all().order_by('id')
    serializer_class = ProductSerializer