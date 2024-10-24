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
def shop(request,slug=None):
    categories = Category.objects.prefetch_related('products', 'children', 'parent')
    subcat = ''


    if slug:
        # Fetch the category by slug
        category = get_object_or_404(Category, slug=slug)
        subcategories = get_subcategories(category)
        subcategories.append(category)

        # Filter products by the selected category and its subcategories
        products = Product.objects.filter(categories__in=subcategories).distinct()
        for subcategory in subcategories:
            # Calculate total products for each subcategory
             total_products= Product.objects.filter(categories=subcategory).count()
             subcategory.total_products_count = total_products


        subcat = subcategories
    else:
        # If no category selected, show all products
        products = Product.objects.all()

    # Calculate total products for each category
    for category in categories:
        subcategories = get_subcategories(category)
        subcategories.append(category)
        total_products = Product.objects.filter(categories__in=subcategories).distinct().count()
        category.total_products_count = total_products

    paginator = Paginator(products, 4)  # Show 10 products per page
    page_number = request.GET.get('page')  # Get the current page number
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  # If page is out of range, deliver last page of results.

    form = ProductSearchForm(request.POST or None)
    results = Product.objects.all()  # Start with all products
    price_limit = None
    query = ''  # Ensure query is always defined, even if empty

    if request.method == 'POST':
        # Check if the form is valid; if invalid, 'query' is already initialized as empty
        if form.is_valid():
            query = form.cleaned_data.get('query', '')

        # Get the price limit from the form input
        price_limit = request.POST.get('price')
        if price_limit:
            try:
                price_limit = float(price_limit)
            except ValueError:
                price_limit = None  # Set to None if conversion fails

        # Apply filters:
        # 1. Filter by product name if query is provided
        if query:
            results = results.filter(name__icontains=query)
            products = results

        # 2. Apply price filter if price_limit is set
        if price_limit is not None and price_limit > 0:
            results = results.filter(price__lte=price_limit)
            products = results



    # Render template with filtered products and categories
    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'form': form,
        'slug': slug,
        'subcat': subcat,
        'paginator': paginator



    })

from django.shortcuts import render
from .models import Product




def shop_detail(request):
    return render(request,'shop-detail.html')

