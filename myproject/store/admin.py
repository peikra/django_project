from django.contrib import admin
from .models import Product, Category


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    filter_horizontal = ('categories',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

