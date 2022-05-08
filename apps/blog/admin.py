from django.contrib import admin

from .models import Tag, Post, Category, Comment, Reply

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Reply)
