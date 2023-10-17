from Services.models.photo_change import PhotoChange
from Services.models.photo_content import PhotoContent, PhotoStateEnum
from api.utils.service_with_result import ServiceWithResult
from Services.service.photo.upload_photo_form_service import UploadPhotoService
from django import forms
from django.conf import settings


class ChangePhotoService(UploadPhotoService):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._photo_base = PhotoContent.objects.get(id=kwargs.pop('photo_id'))
        self.fields['name'].initial = self._photo_base.name
        self.fields['description'].initial = self._photo_base.description



    name = forms.CharField(min_length=3, max_length=45, label='Название')
    media = forms.ImageField(label='фото', required=False)
    description = forms.CharField(required=False, label='Описание')

    @property
    def base_photo_image_profile(self):
        return ''.join([settings.MEDIA_URL, self._photo_base.image_profile.name])

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._save_changes()
        return self


    def run_custom_validations(self):
        if self.cleaned_data[super().MEDIA_FIELD]:
            super()._validate_type_photo()
        super()._validate_name()


    def _save_changes(self):
        if self.cleaned_data[super().MEDIA_FIELD]:
            super()._save_content()
            photo = super().photo
            photo.state = PhotoStateEnum.ON_EDIT
            photo.save()
            change = PhotoChange.objects.create(id_source=self._photo_base, id_update=photo)
            change.save()
        else:
            if self.cleaned_data[super().NAME_FIELD]:
                self._photo_base.name = self.cleaned_data[super().NAME_FIELD]
            if self.cleaned_data[super().DESCRIPTION_FIELD]:
                self._photo_base.description = self.cleaned_data[super().DESCRIPTION_FIELD]

            self._photo_base.save()


