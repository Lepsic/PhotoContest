from datetime import datetime

from Services.tasks import version_photo_created
from api.utils.service_with_result import ServiceWithResult
from django import forms
from Services.models.photo_content import PhotoContent
from django.core.exceptions import ObjectDoesNotExist


class UploadPhotoService(ServiceWithResult):
    CONTENT_TYPE = (['image/png',
                     'image/jpeg',
                     ])
    MEDIA_FIELD = 'media'
    NAME_FIELD = 'name'
    DESCRIPTION_FIELD = 'description'

    custom_validations = ['_validate_name', '_validate_type_photo']


    def __init__(self, *args, **kwargs):
        self._user = kwargs.get('user')
        super(ServiceWithResult, self).__init__(*args)

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._save_content()
        return self

    name = forms.CharField(min_length=3, max_length=45, label='Название')
    media = forms.ImageField(label='Фото')
    description = forms.CharField(required=False, label='Описание')

    def _validate_name(self):
        """Валидация названия"""
        name = self.cleaned_data.get(self.NAME_FIELD)
        if PhotoContent.objects.filter(name=name).exists():
            self.add_error('name', 'Данное имя пользователя уже занято')




    def _validate_type_photo(self):
        """Валидация типа данных"""
        photo_type = self.cleaned_data.get(self.MEDIA_FIELD).content_type
        if photo_type not in self.CONTENT_TYPE:
            self.add_error('media', 'Недопустимый тип файла. Файл должен быть форматом jpg или png')

    def _save_content(self):
        photo = PhotoContent.objects.create(user_id=self._user, name=self.cleaned_data.get(self.NAME_FIELD),
                                            description=self.cleaned_data.get(self.NAME_FIELD),
                                            image=self.cleaned_data.get(self.MEDIA_FIELD),
                                            create_data=datetime.now())
        photo.save()
        version_photo_created(photo)
