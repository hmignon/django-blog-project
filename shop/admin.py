from django.contrib import admin

from .models import Product, ImageAlbum, Image, Color

admin.site.register(Product)
admin.site.register(ImageAlbum)
admin.site.register(Image)
admin.site.register(Color)
