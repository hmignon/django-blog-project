from django.shortcuts import render

from apps.blog.models import BlogCategory, BlogPost
from apps.users.models import User


def index(request):
    all_posts = BlogPost.objects.all().order_by('-first_published_at')
    featured_posts = all_posts.filter(featured=True)[:4]

    context = {
        'featured': featured_posts,
        'latest_posts': all_posts[:8],
        'categories': BlogCategory.objects.all(),
        'owner': User.objects.first(),
        'title': 'Home'
    }

    return render(request, 'home/index.html', context)


def contact(request):
    context = {
        'owner': User.objects.first(),
        'latest_posts': BlogPost.objects.all().order_by('-first_published_at'),

    }
    return render(request, 'home/contact.html', context)


def about(request):
    context = {
        'owner': User.objects.first(),
        'latest_posts': BlogPost.objects.all().order_by('-first_published_at'),

    }
    return render(request, 'home/about.html', context)
