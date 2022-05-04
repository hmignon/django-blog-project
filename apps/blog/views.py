from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from . import utils
from .models import Post, Category, Comment, Reply

QUOTE_OF_THE_DAY = utils.quote_of_the_day()


def post_list(request):
    posts = Post.objects.filter(visible=True).order_by('-date_published')
    context = {
        'posts': posts,
        'featured': posts.first(),
        'qod': QUOTE_OF_THE_DAY,
        'categories': Category.objects.all(),
        'title': "Feed"
    }

    return render(request, 'blog/blog_list.html', context)


def posts_by_category(request, pk):
    category = Category.objects.get(pk=pk)
    filtered_posts = Post.objects.filter(tags__category=category, visible=True).order_by('-date_published')
    context = {
        'posts': filtered_posts,
        'featured': filtered_posts.first(),
        'qod': QUOTE_OF_THE_DAY,
        'categories': Category.objects.all(),
        'title': f"{category.name.title()}"
    }

    return render(request, 'blog/blog_list.html', context)


def post_detail(request, slug, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if post and post.visible is False:
        raise PermissionDenied()
    comments = Comment.objects.filter(post=post)
    replies = Reply.objects.filter(comment__in=comments)

    context = {
        "post": post,
        "comments": comments,
        "replies": replies,
        'title': f"{post.headline}"
    }

    return render(request, 'blog/post_detail.html', context)
