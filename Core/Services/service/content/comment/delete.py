from Services.models.comments import Comments
from Services.service.notification import comment_notification
from rest_framework import status


class DeleteCommentService:
    def __init__(self, user):
        self._error = {}
        self._response_status = status.HTTP_200_OK
        self._result = None
        self._user = user

    def execute(self, service_object_attributes, service_object_files):
        self._delete_comment(service_object_attributes)
        return self

    @property
    def result(self):
        return self._result

    @property
    def errors(self):
        return not bool(self._error)

    @property
    def response_status(self):
        return self._response_status

    def _delete_comment(self, comment_id):
        comment_id = int(comment_id)
        comment = Comments.objects.get(id=comment_id)
        if self._user == comment.user_id:
            if Comments.objects.filter(id=comment_id).exists():
                if Comments.objects.filter(entity_type=1, parent_id_comments_id=comment_id).exists():
                    self._error.update({'_delete_comment': 'This comment not deleted'})
                else:
                    comment.delete()
                    comment_notification(photo_id=comment.parent_id_image.name, user_id=comment.parent_id_image.user_id,
                                         action="DeletedComment",
                                         work_username=self._user.username,
                                         comments_count=str(
                                             Comments.objects.filter(parent_id_image=
                                                                     comment.parent_id_image.id).count()))
