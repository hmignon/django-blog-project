from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=128,
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        required=True,
    )
    message = forms.CharField(
        max_length=8192,
        widget=forms.Textarea(),
        required=True
    )

    class Meta:
        fields = ['name', 'email', 'message']
