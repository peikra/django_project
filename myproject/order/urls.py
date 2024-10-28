from . import views
from django.urls import path

urlpatterns = [
    path('order/cart', views.CartView.as_view(), name='cart'),
    path('order/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/cartitems', views.CartView.as_view(), name='cartitem'),
    path('cartitems/<int:product_id>/', views.DeleteProductView.as_view(), name='delete_product')



]