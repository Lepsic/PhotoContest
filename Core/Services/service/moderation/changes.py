from rest_framework import status
from Services.models.photo_change import PhotoChange


class ChangesService:

    def __init__(self):
        self._error = {}
        self._response_status = status.HTTP_200_OK
        self._result = None

    def execute(self, service_object_attributes, service_object_files):
        getattr(self, service_object_attributes.get('methods'))(service_object_attributes.get('change_id'))
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

    def _approve_changes(self, change_id):
        try:
            change = PhotoChange.objects.get(id_update_id=change_id)
            source_photo = change.id_source
            update_photo = change.id_update
            source_photo.name = update_photo.name
            source_photo.description = update_photo.description
            source_photo.create_data = update_photo.create_data
            source_photo.image = update_photo.image
            source_photo.image_main = update_photo.image_main
            source_photo.image_profile = update_photo.image_profile
            source_photo.save()
            update_photo.finish_edit()
            change.delete()
            self._response_status = status.HTTP_200_OK
        except Exception:
            self._response_status = status.HTTP_400_BAD_REQUEST



    def _reject_changes(self, change_id):
        try:
            change = PhotoChange.objects.get(id_update_id=change_id)
            change.id_update.finish_edit()
            change.delete()
            self._response_status = status.HTTP_200_OK
        except Exception:
            self._response_status = status.HTTP_400_BAD_REQUEST
