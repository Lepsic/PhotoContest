from Services.models.photo_change import PhotoChange
from Services.models.photo_content import PhotoContent
from api.utils.service_with_result import ServiceWithResult


class ChangePhotoService(ServiceWithResult, ):
    def __init__(self, *args, **kwargs):
        self._request_method = kwargs.get('method')
        super(ServiceWithResult, self).__init__(*args)




