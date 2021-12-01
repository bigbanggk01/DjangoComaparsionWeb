from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex 
# Create your models here.
from django.db import models
from django.db.models.fields import CharField, TextField
from django.db import migrations

# Create your models here.
class web_information(models.Model):
    id = models.AutoField(primary_key=True)
    domain = TextField(default='',max_length=40)
    url = TextField(default='',max_length=1000, null=True)
    logo = TextField(default='',max_length=1000, null=False)
    def __str__(self):
        return self.domain
    
class product_xpath(models.Model):
    domain = models.ForeignKey(web_information,on_delete=models.CASCADE)
    item_xpath = models.CharField(max_length=50)
    url_xpath = models.CharField(max_length=50)
    name_xpath = models.CharField(max_length=50)
    price_xpath = models.CharField(max_length=50)
    image_xpath = models.CharField(max_length=100)

class product(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.TextField(max_length=1000)
    name = models.CharField(max_length=5000,null=True)
    price = models.CharField(max_length=20,null=True)
    image_link = models.TextField(max_length=1000)
    description = models.TextField(default='',null=True,max_length=1000)
    brand = models.CharField(default='',null=True, max_length=30)
    category = models.TextField(default='',null=True, max_length=100)
    domain = models.CharField(default='sendo.vn',null=True, max_length=40)
    vector_column = SearchVectorField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = (GinIndex(fields=["vector_column"]),)

class my_category(models.Model):
    name = models.TextField(max_length=200)
    def __str__(self):
        return self.name

class my_subcategory(models.Model):
    parent_category = models.ForeignKey(my_category, on_delete=models.CASCADE)
    name = models.TextField(max_length=200)
    def __str__(self):
        return self.name
