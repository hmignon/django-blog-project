import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now


def path_and_rename(instance, filename):
    upload_to = 'media/blog/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f"{instance.pk}-{instance.name}.{ext}"
    else:
        filename = f"{uuid4().hex}.{ext}"

    return os.path.join(upload_to, filename)


class ImageAlbum(models.Model):
    name = models.CharField(max_length=255)

    def default(self):
        return self.images.filter(default=True).first()

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=path_and_rename)
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, related_name='images')
    default = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, default='slug')

    def __str__(self):
        return f"{self.name} ({self.album})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Image, self).save(*args, **kwargs)


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
    album = models.OneToOneField(ImageAlbum, related_name='album', on_delete=models.CASCADE, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(default=None)
    visible = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, default='slug')

    def __str__(self):
        return f"Post #{self.id}: {self.headline}"

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"pk": self.id, "slug": self.slug})

    def save(self, *args, **kwargs):
        if self.visible is True:
            self.date_published = now()
        else:
            self.date_published = None
        self.slug = slugify(self.headline)

        is_new = True if not self.id else False
        super(Post, self).save(*args, **kwargs)

        if is_new:
            album = ImageAlbum(name=self.headline)
            album.save()
            self.album = album
            self.save()
        else:
            album = ImageAlbum.objects.get(id=self.album_id)
            album.name = self.headline
            album.save()


class Comment(models.Model):
    author_name = models.CharField(max_length=24)
    author_email = models.EmailField()
    content = models.CharField(max_length=1024)
    subscribe = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    author = models.CharField(max_length=24)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now_add=True)
