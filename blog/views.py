from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    posts = Post.objects.filter(visible=True)
    context = {
        'posts': posts,
        'title': "Blog Feed"
    }

    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post and post.visible is False:
        raise PermissionDenied()

    context = {
        "post": post,
        'title': f"{post.title}"
    }

    return render(request, 'blog/post_detail.html', context)
