from django.db import models

# Create your models here.
class website(models.Model):
    weburl = models.TextField(default='', max_length=50)
    searchurl = models.TextField(default='', max_length=300)
    
class navigation_code(models.Model):
    '''
    name -> product name
    url -> product link
    price -> product price
    product code when it have
    web url : any navigation code belongs to a website 
    '''

    '''
    1 = go in
    0 = go down
    '''
    seperator_tag = models.CharField(default='', max_length=10)
    seperator_attr = models.CharField(default='', max_length=20)
    seperator_attr_value = models.CharField(default='', max_length=30)
    name_code = models.CharField(default='',max_length=10)
    url_code = models.CharField(default='',max_length=10)
    price_code = models.CharField(default='',max_length=10)
    product_code_code = models.CharField(default='',max_length=10)
    weburl = models.ForeignKey(website, on_delete=models.CASCADE)