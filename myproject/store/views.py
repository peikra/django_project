from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, F, Sum, Avg
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.views.generic import ListView, TemplateView

from .models import Category, Product, ProductTags
from django.http import JsonResponse
from .forms import ProductSearchForm
from order.models import Cart
from order.models import CartItem



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


# def shop(request, slug=None):
#     categories = Category.objects.prefetch_related('products', 'children', 'parent').filter(parent__isnull=True)
#     subcat = ''
#     products = Product.objects.all()
#     tags = ProductTags.objects.all()
#     for category in categories:
#         subcategories = get_subcategories(category)
#         subcategories.append(category)
#         total_products = Product.objects.filter(categories__in=subcategories).distinct().count()
#         category.total_products_count = total_products
#
#     category='shop'
#
#
#     if slug:
#
#         category = get_object_or_404(Category, slug=slug)
#         subcategories = get_subcategories(category)
#
#         if len(subcategories)==0:
#             subcategories.append(category)
#
#
#
#         products = products.filter(categories__in=subcategories).distinct()
#         for subcategory in subcategories:
#             total_products = Product.objects.filter(categories=subcategory).count()
#             subcategory.total_products_count = total_products
#         subcat = subcategories
#
#     form = ProductSearchForm(request.GET or None)
#     results = Product.objects.all()
#     query = request.GET.get('query', '')
#     price_limit = request.GET.get('price')
#     tag = request.GET.get('tags')
#     sorting_options = request.GET.get('fruitlist')
#
#     if sorting_options!='nothing':
#         if sorting_options=='price':
#             results = results.order_by('price')
#             products = results
#         elif sorting_options=='star':
#             results = results.order_by('-star')
#             products = results
#
#
#     if query:
#         results = results.filter(name__icontains=query)
#         products = results
#
#     if tag:
#         results = results.filter(tags__name=tag)
#         products = results
#
#
#     if price_limit:
#         if int(price_limit)>0:
#             price_limit = float(price_limit)
#             results = results.filter(price__lte=price_limit)
#             products = results
#
#     paginator = Paginator(products, 3)
#     page_number = request.GET.get('page')
#     try:
#         products = paginator.page(page_number)
#     except PageNotAnInteger:
#         products = paginator.page(1)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)
#
#     cart, created = Cart.objects.get_or_create(user=request.user)
#
#
#     total_cart_items = sum(item.quantity for item in cart.items.all())
#
#
#
#
#     return render(request, 'shop.html', {
#         'products': products,
#         'categories': categories,
#         'form': form,
#         'slug': slug,
#         'subcat': subcat,
#         'tags' : tags,
#         'total_cart_items' : total_cart_items,
#         'category':category
#     })
def get_subcategories(category):
    subcategories = category.children.all()
    all_subcategories = list(subcategories)


    for subcategory in subcategories:
        all_subcategories += get_subcategories(subcategory)

    return all_subcategories

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):

        products = Product.objects.all()
        slug = self.kwargs.get('slug')


        if slug:
            category = get_object_or_404(Category, slug=slug)
            subcategories = [category] + get_subcategories(category)
            products = products.filter(categories__in=subcategories).distinct()



        query = self.request.GET.get('query', '')
        price_limit = self.request.GET.get('price')
        tag = self.request.GET.get('tags')
        sorting_options = self.request.GET.get('fruitlist')

        if query:
            products = products.filter(name__icontains=query)
        if price_limit and price_limit.isdigit():
            if int(price_limit)>0:
                products = products.filter(price__lte=float(price_limit))
        if tag:
            products = products.filter(tags__name=tag)


        if sorting_options == 'price':
            products = products.order_by('price')
        elif sorting_options == 'star':
            products = products.order_by('-star')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.prefetch_related('products', 'children', 'parent').filter(parent__isnull=True)
        for category in categories:
            subcategories = get_subcategories(category)
            subcategories.append(category)
            total_products = Product.objects.filter(categories__in=subcategories).distinct().count()
            category.total_products_count = total_products
        subcat = []
        slug = self.kwargs.get('slug')
        context['category'] = 'shop'


        if slug:
            category = get_object_or_404(Category, slug=slug)
            subcategories = get_subcategories(category)
            for subcategory in subcategories:
                total_products = Product.objects.filter(categories=subcategory).count()
                subcategory.total_products_count = total_products
            subcat = subcategories if subcategories else [category]
            context['category'] = category


        context['form'] = ProductSearchForm(self.request.GET or None)
        context['slug'] = slug
        context['subcat'] = subcat
        context['categories'] = categories
        context['tags'] = ProductTags.objects.all()

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['total_cart_items'] = sum(item.quantity for item in cart.items.all())


        else:
            context['total_cart_items'] = 0



        return context



class AddProductView(View):
    def post(self, request, product_id):

        if not request.user.is_authenticated:
            return redirect('login')
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)


        if product.quantity > 0:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += 1
            cart_item.save()
            product.quantity -= 1
            product.save()


        return redirect('shop')


class ShopDetailView(TemplateView):
    template_name = 'shop-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['total_cart_items'] = sum(item.quantity for item in cart.items.all())


        else:
            context['total_cart_items'] = 0

        return context