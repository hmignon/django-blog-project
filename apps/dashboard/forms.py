from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.blog.models import Post


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['headline', 'cover', 'tags', 'summary', 'body']
