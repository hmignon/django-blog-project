from django import template
from apps.blog.models import BlogPost, BlogCategory
from apps.home.models import AboutPage

register = template.Library()


@register.inclusion_tag('include/latest_posts.html')
def latest_posts():
    """ Get list of live blog pages that are descendants of this page """
    posts = BlogPost.objects.live().public().order_by('-first_published_at')[:8]

    return {'latest_posts': posts}


@register.inclusion_tag('include/about_pages.html')
def about_pages():
    about = AboutPage.objects.live()

    return {'about_pages': about}


@register.inclusion_tag('include/categories.html')
def blog_categories():
    categories = BlogCategory.objects.all()

    return {'blog_categories': categories}
