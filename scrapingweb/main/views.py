from django import http
from django.shortcuts import render
from .models import web_information
import sys
import threading
sys.path.append('F:\\Scraping\\myscraper')
import startspider
# Create your views here.

def background_process():
    import time
    print("process started")
    
    print("process finished")

def home(request):
    web_objs = web_information.objects.all()
    contexts = []
    for objs in web_objs:
        if objs.https == True:
            http = 'https'
        else:
            http = 'http'
        domain = objs.domain
        search = objs.query
        context = f'{http}://{domain}/{search}'
        contexts.append(context)
        context = {'contexts':contexts}
    render(request,'main/index.html',context)
    r = startspider.runner(
        [
            ['https://tiki.vn/search?q=', 1]
        ],
        '//a[@class="product-item"]',
        './/@href',
        './/div[@class="name"]/span/text()',
        './/div[@class="price-discount__price"]/text()',
        './/picture[@class="webpimg-container"]/img/@src[1]'
    )
    
    return r.run()

def about(request):
    return render(request,'main/about.html')