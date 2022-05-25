from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.fields import RichTextField
from wagtail.users.forms import UserEditForm, UserCreationForm


class CustomUserEditForm(UserEditForm):
    picture = forms.ImageField()
    summary = forms.CharField(required=True, label=_("Summary"))
    bio = RichTextField()


class CustomUserCreationForm(UserCreationForm):
    picture = forms.ImageField()
    summary = forms.CharField(required=True, label=_("Summary"))
    bio = RichTextField()
