import random
import string
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class ImageAlbum(models.Model):
    name = models.CharField(max_length=255)

    def default(self):
        return self.images.filter(default=True).first()

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/blog/')
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, related_name='images')
    default = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Post(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    body = models.TextField()
    album = models.OneToOneField(ImageAlbum, related_name='album', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(default=None)
    visible = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return f"Post #{self.id}: {self.headline}"

    def save(self, *args, **kwargs):
        if self.visible is True:
            self.date_published = datetime.now()
        else:
            self.date_published = None

        if not self.slug:
            self.slug = slugify(rand_slug() + "_" + self.headline)

        is_new = True if not self.id else False
        super(Post, self).save(*args, **kwargs)
        if is_new:
            album = ImageAlbum(name=self.headline)
            album.save()
            self.album = album
            self.save()
