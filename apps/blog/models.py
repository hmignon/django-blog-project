from django.db import models
from django.forms import CheckboxInput
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page

from . import utils


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
    featured = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('owner'),
        FieldPanel('summary'),
        ImageChooserPanel('cover_image'),
        FieldPanel('body'),
        FieldPanel('featured', widget=CheckboxInput()),
    ]

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return f"Post #{self.id}: {self.title}"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context['latest_posts'] = BlogPost.objects.all().order_by('-first_published_at')
        context['owner'] = self.owner

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
