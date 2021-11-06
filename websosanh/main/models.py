from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import CharField, TextField

# Create your models here.
class web_information(models.Model):
    domain = TextField(default='',max_length=40)
    category = CharField(default='',max_length=100)
    url = TextField(default='',max_length=1000)
    
class product_xpath(models.Model):
    domain = models.ForeignKey(web_information,on_delete=models.CASCADE)
    item_xpath = models.CharField(max_length=50)
    url_xpath = models.CharField(max_length=50)
    name_xpath = models.CharField(max_length=50)
    price_xpath = models.CharField(max_length=50)
    image_xpath = models.CharField(max_length=100)

class product(models.Model):
    url = models.TextField(max_length=1000)
    name = models.CharField(max_length=300,null=True)
    price = models.CharField(max_length=20,null=True)
    image_link = models.TextField(max_length=1000)
    description = models.TextField(default='',null=True,max_length=1000)
    brand = models.CharField(default='',null=True, max_length=30)
    category = models.TextField(default='',null=True, max_length=100)
    def __str__(self):
        return ', '.join(['id=' + str(self.id), 'name=' + self.name, 'url=' + self.url,'description=' + self.description])