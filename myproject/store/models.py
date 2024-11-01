from django.db import models
# Create your models here.
from django.db import models
from versatileimagefield.fields import VersatileImageField
from mptt.models import MPTTModel, TreeForeignKey
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    slug = models.SlugField(unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

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


class ProductTags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    min_weight = models.FloatField(null=True)
    tags = models.ManyToManyField(ProductTags,related_name='product_tags')

    def __str__(self):
        return self.name


