
from django.db import models

from user.models import User
from store.models import Product



# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product.price
        super(CartItem, self).save(*args, **kwargs)


    def get_total_price(self):
        return self.subtotal + self.shipping
