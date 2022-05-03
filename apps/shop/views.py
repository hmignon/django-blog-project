from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from .models import Product


def product_list(request):
    posts = Product.objects.filter(visible=True)
    context = {
        'product': posts,
        'title': "Product List"
    }

    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product and product.visible is False:
        raise PermissionDenied()

    context = {
        'product': product,
        'title': f"{product.name}"
    }

    return render(request, 'shop/product_detail.html', context)
