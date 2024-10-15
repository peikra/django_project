
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('category/', views.category),
    path('category/<int:cat_id>/products/', views.category_products, name='category_products'),
    path('product/<int:product_id>', views.product, name='product'),



]
