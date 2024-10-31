# user/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register , name='register'),
    path('login', views.login_view, name='login'),
    path('home',views.log_out,name='logout')

]
