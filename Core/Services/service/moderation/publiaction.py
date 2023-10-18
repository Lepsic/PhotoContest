from rest_framework import status
from Services.models.photo_content import PhotoContent
from django.core.exceptions import ObjectDoesNotExist


class PublicationService:

    def __init__(self):
        self._error = {}
        self._response_status = status.HTTP_200_OK
        self._result = None
        self._user = None

    def execute(self, service_object_attributes, service_object_files):
        self._approve_publication(service_object_attributes.get('post_id'))
        return self

    @property
    def result(self):
        return self._result

    @property
    def errors(self):
        return self._error

    @property
    def response_status(self):
        return self._response_status

    def _approve_publication(self, post_id):
        try:
            pk = int(post_id)
            photo = PhotoContent.objects.get(id=pk)
            photo.publish()
        except ObjectDoesNotExist as error:
            self._error = error
            self._response_status = status.HTTP_400_BAD_REQUEST


