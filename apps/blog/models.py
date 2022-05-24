from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page

from . import utils


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=255, unique=True, default='slug')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category})"


class BlogPost(Page):
    template = 'blog/post_detail.html'

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    tags = models.ManyToManyField(Tag)
    summary = models.CharField(max_length=200, null=True, blank=True)
    body = RichTextField(null=True, blank=True)
    reading_time = models.PositiveIntegerField(default=1)

    content_panels = Page.content_panels + [
        FieldPanel('owner'),
        FieldPanel('summary'),
        ImageChooserPanel('cover_image'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return f"Post #{self.id}: {self.title}"

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"pk": self.id, "slug": self.slug})

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
