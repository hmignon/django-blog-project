from datetime import datetime

from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20)


class Post(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    tag = models.ForeignKey(to=Tag, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(default=None)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return f"Post #{self.id}: {self.title}"

    def save(self, *args, **kwargs):
        if self.visible is True:
            self.date_published = datetime.now()
        else:
            self.date_published = None
