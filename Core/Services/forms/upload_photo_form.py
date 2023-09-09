from django import forms

from ..service.upload_photo import UploadManager


class UploadPhoto(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_validate = UploadManager(form=self)

    name = forms.CharField(min_length=3, max_length=45, label='Название')
    media = forms.ImageField(label='Фото')
    description = forms.CharField(required=False, label='Описание')

    def clean(self):
        self.service_validate.validate_all()


