from django import forms

from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(
        label="Your name",
        max_length=128,
        widget=forms.TextInput()
    )
    author_email = forms.EmailField(
        label="Your email (will not be displayed)",
        required=True,
    )
    content = forms.CharField(
        label="Comment",
        max_length=8192,
        widget=forms.Textarea(),
        required=True
    )
    subscribe = forms.ChoiceField(
        initial=False,
        label="Subscribe to our newsletter?",
        widget=forms.CheckboxInput(),
        choices=((True, "Yes"), (False, "No"))
    )

    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content', 'subscribe']


class ReplyForm(forms.Form):
    author_name = forms.CharField(
        label="Your name",
        max_length=128,
        widget=forms.TextInput()
    )
    author_email = forms.EmailField(
        label="Your email (will not be displayed)",
        required=True,
    )
    content = forms.CharField(
        label="Comment",
        max_length=8192,
        widget=forms.Textarea(),
        required=True
    )

    class Meta:
        model = Reply
        fields = ['author_name', 'author_email', 'content']
