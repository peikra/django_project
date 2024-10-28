from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView
from order.models import CartItem, Cart
from store.models import Product


# Create your views here.
# order/views.py




class CartView(TemplateView):
    template_name = 'cart.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item_products = CartItem.objects.prefetch_related('product')


        context['products']  = cart_item_products
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['total_cart_items'] = sum(item.quantity for item in cart.items.all())

        return context

class DeleteProductView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get( product=product)
        quantity = cart_item.quantity
        cart_item.delete()
        product.quantity += quantity
        product.save()

        return redirect('cart')



class CheckoutView(TemplateView):
    template_name = 'checkout.html'  # Corrected spelling from 'chackout.html' to 'checkout.html'



