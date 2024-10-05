from . import views
from django.urls import path

urlpatterns = [
    path('products/', views.product),
    path('products/productlist/', views.product_list)


]