import os
from datetime import datetime

from decouple import config
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from loguru import logger
from ..models import PhotoContent
from ..tasks import version_photo_created



class UploadManager:
    content_type = (['image/png',
                     'image/jpeg',
                     ])
    media_field = 'media'
    PhotoDirectory = 'Services/img'

    def __init__(self, request=None, form=None):

        self.request = request
        self.form = form

        # получать из переменной окружения
        self.path_to_static = config('PHOTO_PATH')

        self.validate_data = None
        self.photo = None
        self.path_photo = None
        self.absolute_path_photo = None

    def set_data(self, request=None):
        """Если вдруг напрямую понадобится передать request"""
        self.request = request

    def validate_name(self):
        """Валидация названия"""
        name = self.request.POST['name']
        if PhotoContent.objects.filter(name=name).exists():
            try:
                self.form.add_error('name', 'Данное имя пользователя уже занято')
                return False
            except Exception:
                return False
        else:
            return True

    def __validate_type_photo(self):
        """Валидация типа данных"""
        photo_type = self.request.FILES[self.media_field].content_type
        if isinstance(self.request.FILES[self.media_field], InMemoryUploadedFile) or isinstance(
                self.request.FILES['media'],
                TemporaryUploadedFile):
            if photo_type not in self.content_type:
                self.form.add_error('media', 'Недопустимый тип файла. Файл должен быть форматом jpg или png')
        else:
            self.form.add_error('media', 'Недопустимый тип файла. Файл должен быть форматом jpg или png')

    def validate_all(self):
        """Валидация данных"""
        self.__validate_type_photo()
        self.validate_name()

    def validate_api(self):
        photo_type = self.request.FILES[self.media_field].content_type
        if isinstance(self.request.FILES[self.media_field], InMemoryUploadedFile) or isinstance(
                self.request.FILES[self.media_field],
                TemporaryUploadedFile):
            if photo_type not in self.content_type:
                return 'TypeError'
        else:
            return 'TypeError'
        name = self.request.POST['name']
        if PhotoContent.objects.filter(name=name).exists():
            return 'NameError'

        return True

    # def save_photo(self, photo_form=None):
    #     """Сохранение фото в файловую систему"""
    #     if self.request is not None:
    #         photo = self.request.FILES[self.media_field]
    #     else:
    #         photo = photo_form
    #
    #     name = ''.join([datetime.now().strftime('%Y-%m-%d%H:%M:%S.%f'), photo.name.replace(' ', '')])
    #     self.absolute_path_photo = f'{self.path_to_static}/{self.PhotoDirectory}/{name}'
    #
    #     self.path_photo = f"{self.PhotoDirectory}/{name}"
    #     with open(self.absolute_path_photo, 'wb+') as destination:
    #         for chunk in photo.chunks():
    #             destination.write(chunk)
    #     self.path_photo = f"{settings.STATIC_URL}{self.PhotoDirectory}/{name}"

    def save_content(self, photo_value=None, returned=False):
        """Создание модели и сохранение ее в бд returned - Нужно ли возвращать получившуюся в бд запись"""
        request_data = self.request.POST
        request_photo = self.request.FILES[self.media_field]
        # self.save_photo()
        photo = PhotoContent.objects.create(user_id=self.request.user, name=request_data['name'],
                                            description=request_data['description'], image=request_photo,
                                            create_data=datetime.now())
        photo.save()
        version_photo_created(photo)
        if returned:
            return photo
