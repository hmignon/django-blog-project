from django.shortcuts import get_object_or_404, render

from .models import BlogCategory, BlogPost, PostCategoryRelationship


def blog_list(request):
    posts = BlogPost.objects.live().order_by('-first_published_at')

    context = {
        'posts': posts,
        'title': 'All posts'
    }

    return render(request, 'blog/blog_list.html', context)


def blog_by_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)

    filtered_relationship = PostCategoryRelationship.objects.filter(category=category)
    posts = []
    for relation in filtered_relationship:
        posts.append(BlogPost.objects.get(id=relation.post.id))

    context = {
        'posts': posts,
        'title': f"{category.name}"
    }

    return render(request, 'blog/blog_list.html', context)
