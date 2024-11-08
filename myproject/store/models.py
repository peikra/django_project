from django.db import models
# Create your models here.
from django.db import models
from versatileimagefield.fields import VersatileImageField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name=_('სახელი'))
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name=_('მშობელი'))

    slug = models.SlugField(unique=True,verbose_name=_('სლაგი'))

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
    name = models.CharField(max_length=100,verbose_name=_('სახელი'))

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100,verbose_name=_('სახელი'))
    description = models.TextField(verbose_name=_('აღწერა'))
    price = models.FloatField(verbose_name=_('ფასი'))
    categories = models.ManyToManyField(Category, related_name='products',verbose_name=_('კატეგორია'))
    image = VersatileImageField(upload_to='products/',null=True, blank=True,verbose_name=_('სურათი'))
    quantity = models.IntegerField(default=0,verbose_name=_('რაოდენობა'))
    star = models.IntegerField(default=0,verbose_name=_('ვარსკვლავი'))
    weight = models.FloatField(null=True,verbose_name=_('წონა'))
    country_of_origin = models.TextField(null=True,verbose_name=_('ქვეყნის დასახელება'))
    quality = models.CharField(max_length=50,null=True,verbose_name=_('ხარისხი'))
    min_weight = models.FloatField(null=True,verbose_name=_('მინიმალური წონა'))
    tags = models.ManyToManyField(ProductTags,related_name='product_tags',verbose_name=_('ტეგები'))

    def __str__(self):
        return self.name


