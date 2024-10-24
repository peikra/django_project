from django.db import models
# Create your models here.
from django.db import models
from versatileimagefield.fields import VersatileImageField

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    slug = models.SlugField(unique=True)


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
    image = VersatileImageField(upload_to='products/',null=True, blank=True)
    quantity = models.IntegerField(default=0)
    star = models.IntegerField(default=0)
    weight = models.FloatField(null=True)
    country_of_origin = models.TextField(null=True)
    quality = models.CharField(max_length=50,null=True)
    validate_product = models.CharField(max_length=70,null=True)
    min_weight = models.FloatField(null=True)

    def __str__(self):
        return self.name
