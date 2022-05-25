from django.contrib.auth.models import AbstractUser
from django.db import models

from wagtail.fields import RichTextField


class User(AbstractUser):
    summary = models.CharField(max_length=255, null=True, blank=True)
    bio = RichTextField(null=True, blank=True)
    picture = models.ImageField(upload_to='users/', default='img/default.jpg')


class Subscriber(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
