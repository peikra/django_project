from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView
from order.models import CartItem, Cart
from store.models import Product





class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart.html'
    login_url = 'login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item_products = cart.items.prefetch_related('product')
        context['products'] = cart_item_products

        return context

class DeleteProductView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item = cart.items.get( product=product)
        quantity = cart_item.quantity
        cart_item.delete()
        product.quantity += quantity
        product.save()
        return redirect('cart')



class CheckoutView(TemplateView):
    template_name = 'chackout.html'



