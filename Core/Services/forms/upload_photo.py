from django import forms
from ..service.upload_photo import UploadManager


class UploadPhoto(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_validate = UploadManager(form=self)

    name = forms.CharField(min_length=3, max_length=45)
    media = forms.ImageField()
    description = forms.CharField(required=False)

    def clean(self):
        self.service_validate.validate_all()


