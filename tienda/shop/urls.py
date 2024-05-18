from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('search/', views.search, name='search'),
    path('<str:category>/', views.category_view, name='category_view'),
    path('<str:category>/<str:sku>/', views.product_detail, name='product_detail'),
    path('<str:category>/page/<int:page>/', views.category_view, name='category_view'),
]