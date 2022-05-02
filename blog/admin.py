from django.contrib import admin

from .models import Tag, Post, Image, ImageAlbum, Category

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(ImageAlbum)
admin.site.register(Category)
