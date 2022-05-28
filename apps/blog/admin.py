from django.contrib import admin

from .models import BlogCategory, BlogPost, Comment, Reply

admin.site.register(BlogPost)
admin.site.register(BlogCategory)
admin.site.register(Comment)
admin.site.register(Reply)
