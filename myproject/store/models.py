from django.db import models
# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name





    @property
    def get_parents(self):

        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent
        return parents




class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    categories = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField(upload_to='products/',null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name
