from django import forms


class UploadPhoto(forms.Form):
    name = forms.CharField(min_length=3, max_length=45)
    media = forms.ImageField()
    description = forms.CharField(required=False)
