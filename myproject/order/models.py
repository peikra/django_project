
from django.db import models

from user.models import User




# Create your models here.
class UserCart(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
