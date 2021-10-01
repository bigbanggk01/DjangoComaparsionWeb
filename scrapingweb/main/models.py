from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class web_information(models.Model):
    RENDER_TYPE  = [
        ('NO','No JS render'),
        ('RE','Client side render using JS'),
        ('SC','Render when scroll down JS'),
    ]
    domain = models.CharField(default='',max_length=30, primary_key=True, unique=True)
    query = models.TextField(default='',max_length=200)
    https = models.BooleanField(default=True)
    market = models.BooleanField(default=False)
    render_type = models.CharField(default='NO', max_length=2,choices=RENDER_TYPE)
    
class product_xpath(models.Model):
    domain = models.ForeignKey(web_information,on_delete=models.CASCADE)
    item_xpath = models.CharField(max_length=50)
    url_xpath = models.CharField(max_length=50)
    name_xpath = models.CharField(max_length=50)
    price_xpath = models.CharField(max_length=50)
    image_xpath = models.CharField(max_length=100)

class product(models.Model):
    domain = models.ForeignKey(web_information, on_delete=models.CASCADE)
    url = models.TextField(max_length=300)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=12)
    image_link = models.TextField(max_length=300)
    description = CharField(max_length=40)