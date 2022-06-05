from django.contrib.auth.models import AbstractUser
from django.db import models

from wagtail.fields import RichTextField

from apps.home.models import AboutPage


class User(AbstractUser):
    summary = RichTextField(null=True, blank=True, features=["bold", "italic", "link"])
    picture = models.ImageField(upload_to="users/", default="img/default.jpg")
    about = models.ForeignKey(AboutPage, on_delete=models.CASCADE, null=True, blank=True)


class Subscriber(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
