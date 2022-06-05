from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.home.models import AboutPage
from .models import User


@receiver(post_save, sender=User)
def create_about_page(sender, instance, created, **kwargs):
    if created:
        about = AboutPage.objects.create(
            title=f"About {instance.first_name} {instance.last_name}",
            live=False,
        )
        instance.about = about


@receiver(post_save, sender=User)
def save_about_page(sender, instance, **kwargs):
    instance.about.save()
