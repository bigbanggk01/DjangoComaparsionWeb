from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(product)
admin.site.register(my_category)
admin.site.register(my_subcategory)
admin.site.register(web_information)