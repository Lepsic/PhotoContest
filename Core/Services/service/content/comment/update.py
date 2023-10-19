from rest_framework import status
from Services.models.comments import Comments
from Services.service.content.comment.delete import DeleteCommentService



class UpdateCommentService(DeleteCommentService):
    def __init__(self, user):
        super().__init__(user)
        self._error = {}
        self._response_status = status.HTTP_200_OK
        self._result = None
        self._user = user


    def execute(self, service_object_attributes, service_object_files):
        self._update_comment(service_object_attributes)
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

    def _update_comment(self, data):
        comment_id = int(data['comment_id'])
        comment = Comments.objects.get(id=comment_id)
        if self._user == comment.user_id:
            if data['edit_text'] != '':
                comment.content = data['edit_text']
                comment.save()
            else:
                super()._delete_comment(comment_id)
        else:
            self._error.update({'_update_comment': 'Does not Update Comments'})
