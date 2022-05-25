from django.db import models
from django.forms import CheckboxInput
from django.urls import reverse
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page

from apps.users.models import User
from . import utils


class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_list.html"
    max_count = 1

    content_panels = Page.content_panels

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = BlogPost.objects.live().public().order_by('-first_published_at')

        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])

        context["posts"] = all_posts
        return context


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPost',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )


class BlogPost(Page):
    template = 'blog/post_detail.html'

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    summary = models.CharField(max_length=255, null=True, blank=True)
    body = RichTextField(null=True, blank=True)
    reading_time = models.PositiveIntegerField(default=1)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    featured = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('owner'),
        FieldPanel('summary'),
        ImageChooserPanel('cover_image'),
        FieldPanel('body'),
        FieldPanel('tags'),
        FieldPanel('featured', widget=CheckboxInput()),
    ]

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return f"Post #{self.id}: {self.title}"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        all_posts = BlogPost.objects.all().order_by('-first_published_at')
        context['latest_posts'] = all_posts
        context['owner'] = User.objects.first()
        return context

    def save(self, *args, **kwargs):
        self.reading_time = utils.get_reading_time(str(self.body))
        self.body = utils.cleanup_body_html(str(self.body))

        if not self.summary:
            self.summary = self.body[:200]

        super(BlogPost, self).save(*args, **kwargs)


class Comment(models.Model):
    author_name = models.CharField(max_length=24)
    author_email = models.EmailField()
    content = models.CharField(max_length=1024)
    subscribe = models.BooleanField(default=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)


class Reply(models.Model):
    author_name = models.CharField(max_length=24)
    author_email = models.EmailField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "replies"
