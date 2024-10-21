from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# order/views.py


def cart(request):
    return render(request,'cart.html')

def checkout(request):
    return render(request,'chackout.html')