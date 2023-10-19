from rest_framework import status
from Services.models.photo_content import PhotoContent
from Services.models.comments import Comments
from Services.service.notification import delete_photo_notification
from Services.tasks import schedule_delete_photo
from django.core.exceptions import ObjectDoesNotExist


class DeletePhotoService:

    def __init__(self, user):
        self._error = {}
        self._user = user
        self._response_status = status.HTTP_200_OK
        self._result = None

    class Meta:
        methods = ['_delete', '_cancel_delete']

    def execute(self, service_object_attributes, service_object_files):
        methods = service_object_attributes.get('methods')
        getattr(self, methods)(service_object_attributes.get('data'))
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

    def _delete(self, data):
        try:
            photo_id = data.get('id')
            photo = PhotoContent.objects.get(user_id=self._user, pk=int(data.get('id')))
            photo.initial_delete()
            comments = Comments.objects.filter(parent_id_image=photo)  # Все комментарии к фото
            user_comments = set()  # пользаки, которые оставили комментарии
            for comment in comments:
                user_comments.add(comment.user_id)
            delete_photo_notification(photo, user_comments)
            schedule_delete_photo.delay(photo_id)
        except ObjectDoesNotExist as error:
            self._error = error
            self._response_status = status.HTTP_409_CONFLICT

    def _cancel_delete(self, data):
        try:
            photo = PhotoContent.objects.get(user_id=self._user, pk=int(data.get('id')))
            photo.cancel_delete()
        except ObjectDoesNotExist as error:
            self._error = error
            self._response_status = status.HTTP_409_CONFLICT

