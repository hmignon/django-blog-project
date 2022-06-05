from django import forms
from wagtail.fields import RichTextField
from wagtail.users.forms import UserCreationForm, UserEditForm

from apps.home.models import AboutPage


class CustomUserEditForm(UserEditForm):
    picture = forms.ImageField()
    summary = RichTextField(features=["bold", "italic", "link"])
    about = forms.ModelChoiceField(
        queryset=AboutPage.objects.all(),
        help_text="Select the About page for your profile."
    )


class CustomUserCreationForm(UserCreationForm):
    picture = forms.ImageField()
    summary = RichTextField(features=["bold", "italic", "link"])
    about = forms.ModelChoiceField(
        queryset=AboutPage.objects.all(),
        help_text="Select the About page for your profile."
    )
