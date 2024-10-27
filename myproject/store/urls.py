
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    # path('category/', views.category, name='category'),
    # path('category/<int:cat_id>/products/', views.category_products, name='category_products'),
    # path('product/<int:product_id>', views.product, name='product'),
    path('category/shop/', views.ShopView.as_view(), name='shop'),
    path('category/<slug:slug>/', views.ShopView.as_view(), name='category_products'),
    path('product/shop-detail/', views.ShopDetailView.as_view(), name='shop_detail'),
    path('add_product/<int:product_id>/', views.AddProductView.as_view(), name='add_product'),





]
