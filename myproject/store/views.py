from django.db.models import Count, F, Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Category, Product
from django.http import JsonResponse
from .forms import ProductSearchForm

def get_subcategories(category):
    subcategories = category.children.all()
    all_subcategories = list(subcategories)


    for subcategory in subcategories:
        all_subcategories += get_subcategories(subcategory)

    return all_subcategories
#
#
#
# def category(request):
#     categories = Category.objects.prefetch_related('products','children','parent')
#
#
#     for category in categories:
#         subcategories = get_subcategories(category)
#         subcategories.append(category)
#
#
#         total_products = Product.objects.filter(categories__in=subcategories).distinct().count()
#         category.total_products_count = total_products
#     return render(request,'main.html',{'categories' : categories})
#
#
# def category_products(request, cat_id):
#     category = get_object_or_404(Category, id=cat_id)
#
#     subcategories = get_subcategories(category)
#
#     subcategories.append(category)
#     products = Product.objects.filter(categories__in=subcategories).distinct()
#
#     sum = products.annotate(total=F('quantity') * F('price'))
#     expensive =  products.order_by('-price').first()
#     cheap = products.order_by('price').first()
#     average_price = products.aggregate(average_price=Avg('price'))
#     sub_total = products.annotate(total=F('quantity') * F('price')).aggregate(sub_total=Sum('total'))
#     paginator = Paginator(sum, 3)
#     page = request.GET.get('page')
#
#     page_obj = paginator.get_page(page)
#
#     return render(request, 'product.html', {'category': category,  "sum" : sum,
#                                             'expensive': expensive, 'cheap' :cheap, 'average_price' : average_price,
#                                             'sub_total': sub_total,'page_obj': page_obj,})
#
#
# def product(request,product_id):
#     products = get_object_or_404(Product.objects.prefetch_related('categories'),id=product_id)
#     categories = products.categories.all()
#
#     return render(request,'product_detail.html',{'products':products,'categories':categories})
#
#



#
def shop(request, slug=None):
    categories = Category.objects.prefetch_related('products', 'children', 'parent')
    subcat = ''
    products = Product.objects.all()

    if slug:

        category = get_object_or_404(Category, slug=slug)
        subcategories = get_subcategories(category)
        subcategories.append(category)


        products = products.filter(categories__in=subcategories).distinct()
        for subcategory in subcategories:
            total_products = Product.objects.filter(categories=subcategory).count()
            subcategory.total_products_count = total_products
        subcat = subcategories

    form = ProductSearchForm(request.GET or None)
    results = Product.objects.all()
    query = request.GET.get('query', '')
    price_limit = request.GET.get('price')


    if query:
        results = results.filter(name__icontains=query)
        products = results


    if price_limit:
        if int(price_limit)>0:

            price_limit = float(price_limit)
            results = results.filter(price__lte=price_limit)
            products = results





    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'form': form,
        'slug': slug,
        'subcat': subcat,
    })




def shop_detail(request):
    return render(request,'shop-detail.html')

