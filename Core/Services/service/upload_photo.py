import os

from ..models import PhotoContent
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from datetime import datetime


class UploadManager:
    content_type = (['image/png',
                     ])
    media_field = 'media'
    PhotoDirectory = 'Services/img'

    def __init__(self, request=None, form=None):

        self.request = request
        self.form = form
        self.validate_data = None
        self.photo = None
        # получать из переменной окружения
        self.path_to_static = '/home/lepsic/SaltAndPapperMentorLearn/PhotoContest/Core/Services/static'
        self.path_photo = None

    def set_data(self, request=None):
        self.request = request

    def __validate_name(self):
        name = self.request.POST['name']
        if PhotoContent.objects.filter(name=name).exists():
            self.form.add_error('name', 'Данное имя пользователя уже занято')

    def __validate_type_photo(self):
        """Валидация типа данных"""
        photo_type = self.request.FILES['media'].content_type
        if isinstance(self.request.FILES['media'], InMemoryUploadedFile):
            if photo_type != self.content_type[0]:
                self.form.add_error('media', 'Недопустимый тип файла. Файл должен быть форматом jpg или png')
        else:
            self.form.add_error('media', 'Недопустимый тип файла. Файл должен быть форматом jpg или png')

    def validate_all(self):
        self.__validate_type_photo()
        self.__validate_name()

    def save_photo(self):
        photo = self.request.FILES[self.media_field]

        name = ''.join([datetime.now().strftime('%Y-%m-%d%H:%M:%S.%f'), photo.name.replace(' ', '')])
        absolute_path_photo = '{}/{}/{}'.format(self.path_to_static, self.PhotoDirectory,
                                                name)

        self.path_photo = "{}/{}".format(self.PhotoDirectory, name)
        with open(absolute_path_photo, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)
        self.path_photo = "{}{}/{}".format(settings.STATIC_URL, self.PhotoDirectory, name)

    def save_content(self):
        request_data = self.request.POST
        try:
            self.save_photo()
            photo = PhotoContent.objects.create(user_id=self.request.user, name=request_data['name'],
                                                description=request_data['description'], content=self.path_photo,
                                                create_data=datetime.now())
            photo.save()
        except Exception:
            os.remove('{}/{}'.format(self.path_to_static, self.path_photo))
