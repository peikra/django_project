from django.db.models import Count, F, Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Category, Product
from django.http import JsonResponse





def category(request):


    category = Category.objects.prefetch_related('parent').annotate(product_count=Count('products'))
    return render(request,'index.html',{'category' : category})


def category_products(request, cat_id):

    category = get_object_or_404(Category.objects.prefetch_related('parent'), id=cat_id)
    products = Product.objects.filter(categories=category)


    sum = products.annotate(total=F('quantity') * F('price'))
    expensive =  products.order_by('-price').first()
    cheap = products.order_by('price').first()
    average_price = products.aggregate(average_price=Avg('price'))
    sub_total = products.annotate(total=F('quantity') * F('price')).aggregate(sub_total=Sum('total'))
    paginator = Paginator(sum, 3)
    page = request.GET.get('page')

    page_obj = paginator.get_page(page)

    return render(request, 'product.html', {'category': category,  "sum" : sum,
                                            'expensive': expensive, 'cheap' :cheap, 'average_price' : average_price,
                                            'sub_total': sub_total,'page_obj': page_obj})


def product(request,product_id):
    products = get_object_or_404(Product.objects.prefetch_related('categories'),id=product_id)
    categories = products.categories.all()

    return render(request,'product_detail.html',{'products':products,'categories':categories})



