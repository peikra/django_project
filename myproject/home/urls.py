from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/',views.ContactView.as_view(), name='contact')

]