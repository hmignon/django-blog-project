import re

from django.db import models
from django.forms import RadioSelect
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from . import utils


class BlogPost(Page):
    template = 'blog/post_detail.html'

    # noinspection PyUnresolvedReferences
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
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Blog post'
        verbose_name_plural = 'Blog posts'

    def save(self, *args, **kwargs):
        self.reading_time = utils.get_reading_time(str(self.body))
        self.body = utils.cleanup_body_html(str(self.body))

        if not self.summary:
            """ If 'summary' field is left empty, use start of 'body' and remove html tags """
            self.summary = re.sub(r'<.+?>', '', str(self.body))[:255]

        super(BlogPost, self).save(*args, **kwargs)

    @property
    def categories(self):
        categories = [
            n.category for n in self.post_category_relationship.all()
        ]
        return categories

    def __str__(self):
        return f"Post #{self.id}: {self.title}"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['owner'] = self.owner

        return context

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
        index.SearchField('summary')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('summary'),
        ImageChooserPanel('cover_image'),
        InlinePanel('post_category_relationship', heading="Select post categories"),
        FieldPanel('body'),
        FieldPanel('featured', widget=RadioSelect(choices=[(True, "Yes"), (False, "No")]),
                   heading="Feature this blog post on the home page?"),
    ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default=' ')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog category"
        verbose_name_plural = "Blog categories"


class PostCategoryRelationship(models.Model):
    post = ParentalKey(
        'BlogPost',
        related_name='post_category_relationship'
    )
    category = models.ForeignKey('BlogCategory', related_name="+", on_delete=models.CASCADE)

    panels = [
        FieldPanel('category')
    ]


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
