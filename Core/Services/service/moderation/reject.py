from rest_framework import status
from Services.models.photo_content import PhotoContent, PhotoStateEnum
from Services.tasks import schedule_reject_photo
from django.core.exceptions import ObjectDoesNotExist
from service_objects.errors import InvalidInputsError


class RejectService:

    def __init__(self):
        self._error = {}
        self._response_status = status.HTTP_200_OK
        self._result = None
        self._user = None

    def execute(self, service_object_attributes, service_object_files):
        getattr(self, service_object_attributes.get('methods'))(service_object_attributes.get('post_id'))
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

    def _cancel_reject(self, post_id):
        try:
            photo = PhotoContent.objects.get(id=int(post_id))
            if photo.state == PhotoStateEnum.REJECTED:
                photo.cancel_reject()
            else:
                raise InvalidInputsError
        except ObjectDoesNotExist as error:
            self._error = error
            self._response_status = status.HTTP_400_BAD_REQUEST



    def _reject(self, post_id):
        try:
            pk = int(post_id)
            photo = PhotoContent.objects.get(id=pk)
            photo.initial_reject()
            schedule_reject_photo.delay(pk)
        except ObjectDoesNotExist as error:
            self._error = error
            self._response_status = status.HTTP_400_BAD_REQUEST
