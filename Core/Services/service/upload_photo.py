from ..models import PhotoContent
from django.core.files.uploadedfile import InMemoryUploadedFile
from Core.Core.settings import PHOTO_DIRECTORY


class UploadManager:
    content_type = ('png', 'jpeg')
    media_field = 'media'
    path_photo = None

    def __init__(self, request=None, form=None):
        self.request = request
        self.form = form
        self.validate_data = None
        self.photo = None

    def set_data(self, data, request=None):
        self.validate_data = data
        self.request = request

    def __validate_type_photo(self):
        """Валидация типа данных"""
        photo_type = self.request.FILES('media')
        if isinstance(photo_type, InMemoryUploadedFile):
            if photo_type != self.content_type[0] + '/' + self.content_type[1]:
                self.form.add_error('Недопустимый тип файла. Файл должен быть форматом jpg или png')
        else:
            self.form.add_error('Недопустимый тип файла. Файл должен быть форматом jpg или png')

    # noinspection PyTypeChecker
    def save_photo(self):
        photo = self.request.FILES['media']
        with open(PHOTO_DIRECTORY + '/', photo.name, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)
        self.path_photo = PHOTO_DIRECTORY + '/' + photo.name

    def save_content(self):
        user_id = self.request.user.pk
        photo = PhotoContent.objects.create(user_id=user_id, name=self.validate_data['name'],
                                            description=self.validate_data['description'])
        photo.content.name = self.path_photo
        photo.save()
