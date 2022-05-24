from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import CommentForm, ReplyForm
from .models import BlogPost, Comment, Reply


def post_detail(request, slug, pk=None):
    post = get_object_or_404(BlogPost, pk=pk)
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
        'categories': '',
        'title': f"{post.title}"
    }

    return render(request, 'blog/post_detail.html', context)
