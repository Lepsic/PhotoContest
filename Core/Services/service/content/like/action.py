from Services.models.likes import Likes
from Services.models.photo_content import PhotoContent
from Services.service.notification import like_notification
from rest_framework import status


class ActionLikeService:
    def __init__(self, user=None):
        self._error = {}
        self._user = user
        self._response_status = status.HTTP_200_OK
        self._result = None

    def execute(self, service_object_attributes, service_object_files):
        getattr(self, '_like_action')(service_object_attributes.get('photo_id'))
        return self

    def _like_action(self, photo_id):
        photo = PhotoContent.objects.get(pk=photo_id)
        like = Likes.objects.filter(photo_id=photo, user_id=self._user)
        like_count = Likes.objects.filter(photo_id=photo_id).count()
        if like.exists():
            like_count -= 1
            like.delete()
            like_notification(user_id=photo.user_id, like_id=photo.name, action="DeletedLike",
                              work_username=self._user.username,
                              like_count=str(like_count))
            self._result = {"count_likes": str(like_count)}
        else:
            like_count += 1
            like = Likes.objects.create(user_id=self._user, photo_id=photo)
            like.save()
            like_notification(user_id=photo.user_id, like_id=like.photo_id.name, action="CreatedLike",
                              work_username=self._user.username,
                              like_count=str(like_count))
            self._result = {"count_likes": str(like_count)}

    @property
    def response_status(self):
        return self._response_status

    @property
    def errors(self):
        return self._error

    @property
    def result(self):
        return self._result