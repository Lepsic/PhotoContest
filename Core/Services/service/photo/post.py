from datetime import datetime

from Services.models.photo_content import PhotoContent, PhotoStateEnum
from rest_framework import status

from Services.tasks import version_photo_created


class PostPhotoService:
    CONTENT_TYPE = (['image/png',
                     'image/jpeg',
                     ])


    def __init__(self, user):
        self._error = {}
        self._user = user
        self._response_status = None
        self._result = None


    def execute(self, data):
        self._validate_type_photo(data)
        self._validate_name(data)
        if not bool(self.errors):
            self._save_photo(data)
            return self


    @property
    def errors(self):
        return self._error

    @property
    def response_status(self):
        return self._response_status

    @property
    def result(self):
        return self._result

    def _save_photo(self, data):
        photo = PhotoContent.objects.create(user_id=self._user, name=data.get('name'),
                                            description=data.get('description'),
                                            image=data.get('media'),
                                            create_data=datetime.now())
        photo.save()
        version_photo_created(photo)
        self._result = photo



    def _validate_type_photo(self, data):
        photo_type = data.get('media').content_type
        if photo_type not in self.CONTENT_TYPE:
            self._error = {'_validate_type_photo': 'Type validation failed'}
            self._response_status = status.HTTP_404_NOT_FOUND

    def _validate_name(self, data):
        name = data.get('name')
        if PhotoContent.objects.filter(name=name).exists():
            self._error.update({'_validate_name': 'Name validation failed'})
            self._response_status = status.HTTP_404_NOT_FOUND
