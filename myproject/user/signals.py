from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User  # Ensure absolute import
from order.models import UserCart  # Ensure absolute import

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserCart.objects.create(user=instance)