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
    template = "blog/post_detail.html"

    # noinspection PyUnresolvedReferences
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="+",
        help_text="Choose a cover image for your blog post to feature on your home page and post category lists."
    )
    summary = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=("Write a short summary (max 255 characters) for your blog post. If left empty, the summary will be "
                   "replaced by the start of the blog post body. ")
    )
    body = RichTextField(
        null=True,
        blank=True,
        help_text=("Your blog post content. You can add headers, links, numbered lists and bullet points, images, "
                   "embedded content, etc. ")
    )
    reading_time = models.PositiveIntegerField(default=1)
    featured = models.BooleanField(
        default=False,
        help_text=("If featured, the published post will be displayed on the home page. Only the latest 4 featured "
                   "posts will be displayed.")
    )

    class Meta:
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"

    def __str__(self):
        return f"Post #{self.id}: {self.title}"

    def save(self, *args, **kwargs):
        body_clean = re.sub(r'<.+?>', '', str(self.body))
        self.reading_time = utils.get_reading_time(str(body_clean))
        # self.body = utils.cleanup_body_html(str(self.body))

        if not self.summary:
            """If 'summary' field is left empty, use start of 'body' and remove html tags."""
            self.summary = body_clean[:255]

        super(BlogPost, self).save(*args, **kwargs)

    @property
    def categories(self):
        categories = [
            n.category for n in self.post_category_relationship.all()
        ]
        return categories

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["author"] = self.owner

        return context

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("body"),
        index.SearchField("summary")
    ]

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        ImageChooserPanel("cover_image"),
        InlinePanel("post_category_relationship", heading="Select post category / subcategory:",
                    help_text="Select one category and/or one subcategory."),
        FieldPanel("body"),
        FieldPanel("featured", widget=RadioSelect(choices=[(True, "Yes"), (False, "No")]),
                   heading="Feature this blog post on the home page?"),
    ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default='', blank=True, null=True)

    class Meta:
        verbose_name = "Blog category"
        verbose_name_plural = "Blog categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)


@register_snippet
class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default='', blank=True, null=True)
    category = models.ForeignKey("BlogCategory", on_delete=models.CASCADE, related_name="sub_categories")

    class Meta:
        verbose_name = "Sub category"
        verbose_name_plural = "Sub categories"

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)


class PostCategoryRelationship(models.Model):
    post = ParentalKey(
        "BlogPost",
        related_name="post_category_relationship"
    )
    category = models.ForeignKey("BlogCategory", related_name="+", on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey("SubCategory", related_name="+", on_delete=models.CASCADE, null=True, blank=True)

    panels = [
        FieldPanel("category"),
        FieldPanel("sub_category")
    ]

    def save(self, *args, **kwargs):
        if self.sub_category and not self.category:
            self.category = self.sub_category.category
        super(PostCategoryRelationship, self).save(*args, **kwargs)


class Comment(models.Model):
    author_name = models.CharField(max_length=24)
    author_email = models.EmailField()
    content = models.CharField(max_length=1024)
    subscribe = models.BooleanField(default=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    date_created = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)


class Reply(models.Model):
    author_name = models.CharField(max_length=24)
    author_email = models.EmailField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    content = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "replies"
