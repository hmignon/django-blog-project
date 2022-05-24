from django.shortcuts import render

from apps.blog.models import BlogPost, Category


def index(request):
    featured_post = BlogPost.objects.first()
    context = {
        'featured': featured_post,
        'categories': Category.objects.all(),
        'title': "Home"
    }

    return render(request, 'home/index.html', context)


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')
