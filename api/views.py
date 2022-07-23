from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    context = {
        'index_title': 'WELCOME!',
        'index_text': 'my API-backend',
    }
    return render(request, 'index.html', context)

def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404,
    )

def server_error(request):
    return render(
        request,
        'misc/500.html',
        status=500
    )

def product(request):
    context = {
        'product_title': 'ABOUT SITE',
        'product_text': 'readme',
    }
    return render(request, 'product.html', context)
