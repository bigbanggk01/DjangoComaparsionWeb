from django.contrib.postgres import search
from django.db.models import query
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import product,my_category,my_subcategory, web_information
from .serializers import ProductSerializer
from rest_framework import generics
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
PRODUCT_PER_PAGE = 60
def home(request):
    q = request.GET.get('q')
    if q is not None:
        return redirect('/main/?q='+q)
    else:
        categories = my_category.objects.all()
        subcategories = my_subcategory.objects.all()
        products = product.objects.all().order_by('id')[:12]
        websites = web_information.objects.all().order_by('id')[:19]
        context = {
            'categories':categories,
            'subcategories':subcategories,
            'products':products,
            'websites':websites
        }
               
        return render(request,'main/home.html',context)   

def index(request):
    context = {}
    query = ""
    if request.GET:
        query = request.GET.get('q','')
        context['query'] = str(query)
    # products = product.objects.annotate(search=SearchVector('name')).filter(query).order_by('id')
    myquery = SearchQuery(query)
    rank = SearchRank(F('vector_column'), query)

    products = product.objects.annotate(rank=rank).filter(vector_column=myquery).order_by('-rank')
    context['products'] = products
    categories = my_category.objects.all()
    subcategories = my_subcategory.objects.all()

    context['categories'] = categories 
    context['subcategories'] = subcategories
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