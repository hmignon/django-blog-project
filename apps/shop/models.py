import random
import string

from django.db import models
from django.utils.text import slugify


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


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
    image = models.ImageField(upload_to='media/shop/')
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE, related_name='images')
    default = models.BooleanField(default=False)


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
