

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from order.models import Cart
# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['total_cart_items'] = sum(item.quantity for item in cart.items.all())

        return context

class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['total_cart_items'] = sum(item.quantity for item in cart.items.all())

        return context