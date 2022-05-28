from django.shortcuts import render

from .models import ProductPage


def product_list(request):
    products = ProductPage.objects.all()
    context = {
        'title': "Product List",
        'products': products
    }

    return render(request, 'shop/product_list.html', context)
