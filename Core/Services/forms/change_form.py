from django import forms


class ChangePhoto(forms.Form):
    name = forms.CharField(min_length=3, max_length=45, label='Название')
    media = forms.ImageField(label="фото", required=False)
    description = forms.CharField(required=False, label='Описание')

