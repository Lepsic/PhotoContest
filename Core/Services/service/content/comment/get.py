from Services.models.comments import Comments
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


class GetCommentService:
    arguments_dict = {'photo_id': '_get_comment', 'comment_id': '_get_content_comment'}

    def __init__(self):
        self._error = {}
        self._response_status = status.HTTP_200_OK
        self._result = None

    def execute(self, service_object_attributes, service_object_files):
        action = str((set(self.arguments_dict.keys()) & set(service_object_attributes.keys())).pop())
        getattr(self, self.arguments_dict.get(action))(service_object_attributes.get(action))
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

    def _get_comment(self, photo_id):
        comments = Comments.objects.filter(parent_id_image_id=int(photo_id))
        response = {'data': []}
        for comment in comments:
            if comment.entity_type == 0:
                count_child_comment = Comments.objects.filter(parent_id_image_id=1,
                                                              parent_id_comments_id=comment.id).count()
                response['data'].append({
                    'id': comment.id,
                    'username': comment.user_id.username,
                    'content': comment.content,
                    'count_child_comments': count_child_comment,
                    'child_comments': False,
                    'user_id': comment.user_id.pk
                })
            if comment.entity_type == 1:
                response['data'].append({
                    'id': comment.id,
                    'username': comment.user_id.username,
                    'content': comment.content,
                    'child_comment': True,
                    'parent_id': comment.parent_id_comments_id,
                    'user_id': comment.user_id_id
                })
        self._result = response


    def _get_content_comment(self, comment_id):
        try:
            comment_id = int(comment_id)
            comment = Comments.objects.get(id=comment_id)
            self._result = {'commentContent': comment.content}
        except ObjectDoesNotExist:
            self._error = {'_get_content_comment': 'Comment does not exist'}
            self._response_status = status.HTTP_404_NOT_FOUND
