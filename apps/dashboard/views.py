from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from apps.blog.models import Post
from .forms import PostForm


@login_required
def index(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def post_list(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'title': 'Posts'
    }

    return render(request, 'dashboard/post_list.html', context)


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    context = {
        'title': post.headline,
        'post': post
    }

    return render(request, 'dashboard/post_detail.html', context)


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                cover = request.FILES['cover']
            except MultiValueDictKeyError:
                cover = None

            post = Post.objects.create(
                author=request.user,
                headline=request.POST['headline'],
                cover=cover,
                summary=request.POST['summary'],
                body=request.POST['body']
            )

            return redirect(reverse('dashboard:post_detail', kwargs={'pk': post.pk}))

    else:
        form = PostForm()

    context = {
        'form': form,
        'title': 'New post',
    }

    return render(request, 'dashboard/post_new.html', context)
