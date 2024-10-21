from . import views
from django.urls import path

urlpatterns = [
    path('order/cart', views.cart, name='cart'),
    path('order/checkout/', views.checkout, name='checkout')



]