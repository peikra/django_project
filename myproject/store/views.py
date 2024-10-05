from django.http import HttpResponse

# Create your views here.
def product(request):
    return HttpResponse( "პროდუქტები:")


def product_list(request):
    products = {'შაქარი' : '2ლ', 'მარილი' : "1.50ლ", "პური" : '1ლ', 'კვერცხი': "0.50ლ"}
    return HttpResponse(f'{products}')