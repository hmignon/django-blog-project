import os
from uuid import uuid4

from PIL import ImageOps, Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now

from . import utils


def path_and_rename(instance, filename):
    upload_to = 'blog/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f"{instance.pk}-{instance.headline}.{ext}"
    else:
        filename = f"{uuid4().hex}.{ext}"

    return os.path.join(upload_to, filename)


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


class Post(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    cover = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    summary = models.CharField(max_length=200, null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    reading_time = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(default=None, null=True)
    visible = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, default='')

    def __str__(self):
        return f"Post #{self.id}: {self.headline}"

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"pk": self.id, "slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline)
        self.reading_time = utils.get_reading_time(self.body)
        self.body = utils.cleanup_body_html(self.body)

        if not self.summary:
            self.summary = self.body[:200]

        if self.visible is True:
            self.date_published = now()
        else:
            self.date_published = None

        if self.cover:
            img = ImageOps.contain(
                Image.open(self.cover.path),
                (1200, 1200),
                method=3
            )

            img.save(self.cover.path)

        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    author_name = models.CharField(max_length=24)
    author_email = models.EmailField()
    content = models.CharField(max_length=1024)
    subscribe = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
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
