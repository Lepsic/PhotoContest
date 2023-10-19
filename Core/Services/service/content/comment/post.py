from rest_framework import status
from Services.models.comments import Comments
from Services.models.photo_content import PhotoContent
import datetime

from Services.service.notification import comment_notification


class PostCommentService:
    def __init__(self, user):
        self._error = {}
        self._response_status = status.HTTP_200_OK
        self._result = None
        self._user = user

    def execute(self, service_object_attributes, service_object_files):
        self._post_comments(service_object_attributes)
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

    def _post_comments(self, post_data):
        if post_data['parent_id_comment'] == 'true':
            photo = Comments.objects.get(id=post_data['parent_id']).parent_id_image
            comment = Comments.objects.create(user_id=self._user, content=post_data['content'],
                                              parent_id_image_id=photo.id, entity_type=1,
                                              parent_id_comments_id=post_data['parent_id'],
                                              create_time=datetime.datetime.now())
        if post_data['parent_id_comment'] == 'false':
            photo = PhotoContent.objects.get(id=post_data['image_id'])
            comment = Comments.objects.create(user_id=self._user, content=post_data['content'],
                                              parent_id_image_id=photo.id, entity_type=0,
                                              create_time=datetime.datetime.now())
        comment.save()
        response = {'comment_id': comment.id}
        if comment.entity_type == 1:
            response.update({'comment_parent_id': comment.parent_id_comments.id})

        comment_notification(photo_id=photo.name, user_id=photo.user_id, action="CreatedComment",
                             work_username=self._user.username,
                             comments_count=str(Comments.objects.filter(parent_id_image=photo).count()))
        self._result = response
