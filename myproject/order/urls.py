from . import views
from django.urls import path

urlpatterns = [
    path('orders/', views.orders),
    path('orders/orderlist/', views.order_list)


]