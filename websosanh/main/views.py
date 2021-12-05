from django.contrib.postgres import search
from django.shortcuts import redirect, render
from .models import product,my_category,my_subcategory, web_information
from .serializers import ProductSerializer
from rest_framework import generics
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
from sklearn import preprocessing
import pickle

PRODUCT_PER_PAGE = 60
def home(request):
    q = request.GET.get('q')
    if q is not None:
        return redirect('/main/?q='+q)
    else:
        categories = my_category.objects.filter(public=True).order_by('id')[:20]
        subcategories = my_subcategory.objects.all()
        myquery = SearchQuery('Điện thoại samsung')
        products = product.objects.filter(vector_column=myquery,mycat=3).order_by('id')[:10]
        websites = web_information.objects.all().order_by('id')[:19]
        context = {
            'categories':categories,
            'subcategories':subcategories,
            'products':products,
            'websites':websites
        }
               
        return render(request,'main/home.html',context)   

def prod(request):
    context = {}
    query = ""
    if request.GET:
        query = request.GET.get('cat','')
        if query != '':
            context['query'] = str(query)
            products = product.objects.filter(mycat=query).order_by('-id')[:1000]
            context['products'] = products
            categories = my_category.objects.filter(public=True).order_by('id')[:20]
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
        else:
            query = request.GET.get('q','')
            context['query'] = str(query)

            myquery = SearchQuery(query)
            rank = SearchRank(F('vector_column'), query)

            #Ai
            file_clf_open = open("F:\Scraping\clf", "rb")
            loaded_clf = pickle.load(file_clf_open)
            file_clf_open.close()
            file_lb_open = open("F:\Scraping\lb", "rb")
            loaded_lb = pickle.load(file_lb_open)
            file_lb_open.close()

            vt = loaded_lb.transform(query.split()).sum(axis=0).reshape(1, -1)
            mycat = loaded_clf.predict(vt)
            products = product.objects.annotate(rank=rank).filter(vector_column=myquery,mycat=mycat[0]).order_by('-rank')
            context['products'] = products
            categories = my_category.objects.filter(public=True).order_by('id')[:20]
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

def register(request):
    username = request.POST.get('username')
    if username is None or username=='':
        return render(request, 'main/register.html')
    else:
        return render(request,'<h1>yes</h1>') 

class GetAllProductAPIView(generics.ListCreateAPIView):
    queryset = product.objects.all().order_by('id')
    serializer_class = ProductSerializer