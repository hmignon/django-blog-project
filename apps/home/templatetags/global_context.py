from django import template

from apps.blog.forms import CommentForm, ReplyForm
from apps.blog.models import BlogPost, BlogCategory, SubCategory
from apps.home.models import AboutPage
from apps.users.models import User

register = template.Library()


@register.inclusion_tag("include/latest_posts.html")
def latest_posts():
    """ Get list of live blog pages that are descendants of this page """
    posts = BlogPost.objects.live().public().order_by("-first_published_at")[:8]

    return {'latest_posts': posts}


@register.inclusion_tag("include/about_pages.html")
def about_pages():
    about = AboutPage.objects.live()

    return {'about_pages': about}


@register.inclusion_tag("include/categories.html")
def blog_categories():
    categories = BlogCategory.objects.all()

    return {'blog_categories': categories}


@register.inclusion_tag("include/sub_categories.html")
def sub_categories(category):
    subs = SubCategory.objects.filter(category=category)

    return {'subs': subs}


@register.inclusion_tag("include/comment_form.html")
def comment_form():
    c_form = CommentForm()
    r_form = ReplyForm()

    return {
        "c_form": c_form,
        "r_form": r_form
    }


@register.inclusion_tag("include/post_filter.html")
def post_filter():
    categories = BlogCategory.objects.all()
    subcategories = SubCategory.objects.all()
    authors = User.objects.all()

    return {
        "categories": categories,
        "subcategories": subcategories,
        "authors": authors,
    }
