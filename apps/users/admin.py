from django.contrib import admin

from apps.users.models import Subscriber, User

admin.site.register(User)
admin.site.register(Subscriber)
