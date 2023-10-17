from rest_framework import status
from Services.service.photo.post import PostPhotoService
from Services.models.photo_content import PhotoContent, PhotoStateEnum
from api.utils.service_outcome import ServiceOutcome
from Services.models.photo_change import PhotoChange


class UpdatePhotoService:
    def __init__(self, user):
        self._error = {}
        self._user = user
        self._response_status = status.HTTP_200_OK
        self._result = None
        self._base_photo = None

    def execute(self, data):
        self._result = self._change_photo(data)

    @property
    def errors(self):
        return self._error

    @property
    def response_status(self):
        return self._response_status

    @property
    def result(self):
        return self._result

    def _set_photo(self, pk):
        photo = PhotoContent.objects.get(id=pk)
        self._base_photo = photo


    def _change_photo(self, data):
        self._set_photo(data['photo_source_id'])
        if data['media']:
            photo_created_data = {'name': data['name'], 'description': data['description'], 'media': data['media']}
            outcome = ServiceOutcome(PostPhotoService(self._user), photo_created_data)
            if bool(outcome.valid):
                change = PhotoChange.objects.create(id_source=self._base_photo, id_update=outcome.result)
                outcome.result.state = PhotoStateEnum.ON_EDIT
                outcome.result.save()
                change.save()
                return change
            else:
                self._response_status = outcome.response_status
                self._error = outcome.errors


        self._base_photo.name = data['name']
        self._base_photo.description = data['description']
        self._base_photo.save()
        return  self._base_photo

