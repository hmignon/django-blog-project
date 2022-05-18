from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from . import utils
from .forms import CommentForm, ReplyForm
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


def posts_by_category(request, slug):
    category = Category.objects.get(slug=slug)
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
    comments = Comment.objects.filter(post=post, moderated=True)
    replies = Reply.objects.filter(comment__in=comments)

    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        r_form = ReplyForm(request.POST)

        if c_form.is_valid():
            Comment.objects.create(
                author_name=request.POST['author_name'],
                author_email=request.POST['author_email'],
                content=request.POST['content'],
                subscribe=request.POST['subscribe'],
                post=post
            )

            return redirect(reverse('blog:detail', kwargs={'pk': pk, 'slug': slug}))

        elif r_form.is_valid():
            Reply.objects.create(
                author_name=request.POST['author_name'],
                author_email=request.POST['author_email'],
                content=request.POST['content'],
                comment=comments.first()
            )

            return redirect(reverse('blog:detail', kwargs={'pk': pk, 'slug': slug}))

    else:
        c_form = CommentForm()
        r_form = ReplyForm()

    context = {
        'c_form': c_form,
        'r_form': r_form,
        "post": post,
        "comments": comments,
        "replies": replies,
        'qod': QUOTE_OF_THE_DAY,
        'categories': Category.objects.all(),
        'title': f"{post.headline}"
    }

    return render(request, 'blog/post_detail.html', context)
