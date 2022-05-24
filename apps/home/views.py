from django.shortcuts import render

from apps.blog.models import BlogPost
from apps.users.models import User


def index(request):
    all_posts = BlogPost.objects.all().order_by('-first_published_at')
    featured_post = all_posts.first()
    posts = all_posts.exclude(id=featured_post.id)

    context = {
        'featured': featured_post,
        'posts': all_posts,
        'categories': '',
        'owner': User.objects.first(),
        'title': "Home"
    }

    return render(request, 'home/index.html', context)


def contact(request):
    return render(request, 'home/contact.html')


def about(request):
    context = {'user': User.objects.first()}
    return render(request, 'home/about.html', context)
