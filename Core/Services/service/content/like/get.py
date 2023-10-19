from Services.models.likes import Likes
from Services.models.photo_content import PhotoContent
from rest_framework import status
class GetLikeService:
    def __init__(self, user=None):
        self._error = {}
        self._user = user
        self._response_status = status.HTTP_200_OK
        self._result = None

    def execute(self, service_object_attributes, service_object_files):
        getattr(self, '_like_count')(service_object_attributes.get('photo_id'))
        return self

    def _like_count(self, photo_id):
        self._result = {'count_likes': str(Likes.objects.filter(photo_id=photo_id).count())}

    @property
    def response_status(self):
        return self._response_status

    @property
    def errors(self):
        return self._error

    @property
    def result(self):
        return self._result