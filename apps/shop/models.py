import os
from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def path_and_rename(instance, filename):
    upload_to = 'shop/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f"{instance.pk}-{instance.name}.{ext}"
    else:
        filename = f"{uuid4().hex}.{ext}"

    return os.path.join(upload_to, filename)


class Color(models.Model):
    name = models.CharField(max_length=20)
    hex_code = models.CharField(max_length=6)


class ImageAlbum(models.Model):
    name = models.CharField(max_length=20)

    def default(self):
        return self.images.filter(default=True).first()

    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=path_and_rename)
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, related_name='images')
    default = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, default='')

    def __str__(self):
        return f"{self.name} ({self.album})"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Image, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    colors = models.ManyToManyField(Color)
    in_stock = models.PositiveIntegerField()
    album = models.OneToOneField(ImageAlbum, related_name='album', on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, default='slug')

    def __str__(self):
        return f"Product #{self.id}: {self.name}"

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail', kwargs={"pk": self.id, "slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        is_new = True if not self.id else False
        super(Product, self).save(*args, **kwargs)
        if is_new:
            album = ImageAlbum(name=self.name)
            album.save()
            self.album = album
            self.save()