
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from order.models import Cart
from store.models import Category
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True)
        context['categories'] = categories
        return context




class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name", "")
        message = request.POST.get("message", "")
        from_email = request.POST.get("email", "")
        subject = f"Message from {name}"

        if name and message and from_email:
            try:
                send_mail(subject, message, from_email, ["peikrishvilimisho99@gmail.com"])
                messages.success(request, "მესიჯი წარმატებით გაიგზავნა")
                return redirect('contact')
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")

        return redirect('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True)
        context['categories'] = categories
        return context
