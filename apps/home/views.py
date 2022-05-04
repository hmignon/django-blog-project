from django.shortcuts import render

from apps.blog.models import Post, Category
from apps.blog.views import QUOTE_OF_THE_DAY


def index(request):
    featured_post = Post.objects.filter(visible=True).order_by('-date_published').first()
    context = {
        'featured': featured_post,
        'qod': QUOTE_OF_THE_DAY,
        'categories': Category.objects.all(),
        'title': "Home"
    }

    return render(request, 'home/index.html', context)


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')
