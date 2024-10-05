from django.http import HttpResponse

# Create your views here.
# order/views.py


def orders(request):
    return HttpResponse("შეკვეთები:")

def order_list(request):
    return HttpResponse(f"თქვენ შეუკვეთეთ პური და შაქარი")
