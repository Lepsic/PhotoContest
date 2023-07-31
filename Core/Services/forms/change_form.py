from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils.html import format_html


class ChangePhoto(forms.Form):
    name = forms.CharField(min_length=3, max_length=45, label='Название')
    media = forms.ImageField(label="фото", required=False)
    description = forms.CharField(required=False, label='Описание')

