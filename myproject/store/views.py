from django.http import HttpResponse
from .models import Category, Product
from django.http import JsonResponse

def category(request):
    categories = Category.objects.all()
    category_data = []

    for category in categories:
        category_data.append({
            'id': category.id,
            'name': category.name,
            'parent_name_id': [category.parent.name, category.parent.id] if category.parent else None
        })

    return JsonResponse({'categories': category_data}, safe=False)





def get_last_parent_category(categories):

    for category in categories:

        if category.children.count() == 0:
            return category.name

    return categories.first().name if categories.exists() else None



def product(request):
    products = Product.objects.all()
    product_data = []

    for product in products:

        categories = product.categories.all()

        last_parent_category = get_last_parent_category(categories)

        product_data.append({
            'id': product.id,
            'name': product.name,
            'category': last_parent_category
        })

    return JsonResponse({'products': product_data}, safe=False)


