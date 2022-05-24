from django.contrib import admin

from .models import Tag, BlogPost, Category, Comment, Reply

admin.site.register(Tag)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Reply)
