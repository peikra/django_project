from order.models import Cart

def cart_items_count(request):
    total_cart_items = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_cart_items = sum(item.quantity for item in cart.items.all())

    return {
        'total_cart_items': total_cart_items
    }