
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('products/', views.product),
    path('products/productlist/', views.product_list)


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)