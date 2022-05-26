from django.shortcuts import render

from apps.users.models import User
from .models import BlogPost


def blog_list(request):
    all_posts = BlogPost.objects.all().order_by('-first_published_at')

    context = {
        'latest_posts': all_posts,
        'categories': '',
        'owner': User.objects.first(),
        'title': 'Blog'
    }

    return render(request, 'blog/blog_list.html', context)
