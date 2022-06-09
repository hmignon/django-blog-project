from django.shortcuts import get_object_or_404, render

from .models import BlogCategory, BlogPost, PostCategoryRelationship, SubCategory


def blog_list(request):
    posts = BlogPost.objects.live().order_by("-first_published_at")
    categories = BlogCategory.objects.all()

    context = {
        "posts": posts,
        "categories": categories,
        "title": "All posts"
    }

    return render(request, "blog/blog_list.html", context)


def blog_by_category(request, category_slug, sub_slug):
    category = get_object_or_404(BlogCategory, slug=category_slug)

    if sub_slug == 'all':
        filtered_relationship = PostCategoryRelationship.objects.filter(category=category)
        title = f"{category.name} - All posts"
        posts = []
        for relation in filtered_relationship:
            posts.append(BlogPost.objects.get(id=relation.post.id))
    else:
        sub = get_object_or_404(SubCategory, slug=sub_slug)
        filtered_relationship = PostCategoryRelationship.objects.filter(sub_category=sub)
        title = f"{category.name} - {sub.name}"
        posts = []
        for relation in filtered_relationship:
            posts.append(BlogPost.objects.get(id=relation.post.id))

    context = {
        "posts": posts,
        "title": title
    }

    return render(request, "blog/blog_list.html", context)
