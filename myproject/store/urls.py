
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('category/', views.category),
    path('category/product/', views.product)


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)