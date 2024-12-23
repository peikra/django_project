from django.contrib import admin
from .models import Product, Category, ProductTags


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    filter_horizontal = ('categories',)
@admin.register(ProductTags)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



