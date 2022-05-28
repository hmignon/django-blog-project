from django import forms
from wagtail.fields import RichTextField
from wagtail.users.forms import UserCreationForm, UserEditForm


class CustomUserEditForm(UserEditForm):
    picture = forms.ImageField()
    summary = RichTextField(features=['bold', 'italic', 'link'])
    bio = RichTextField()


class CustomUserCreationForm(UserCreationForm):
    picture = forms.ImageField()
    summary = RichTextField(features=['bold', 'italic', 'link'])
    bio = RichTextField()
