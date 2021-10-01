from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(web_information)
class WebAdmin(admin.ModelAdmin):
    pass
@admin.register(product_xpath)
class XPathAdmin(admin.ModelAdmin):
    pass
@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    pass
