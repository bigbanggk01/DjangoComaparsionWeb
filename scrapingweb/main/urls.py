from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='views-index'),
    path('about/', views.about, name='views-about'),
]