from ..models import PhotoContent
import base64
from PIL import Image
from io import BytesIO


class PhotoManager:
    """Класс для взаимодействия с картинками"""

    ACTION_TO_RESIZE = {'profile': (200, 300)}

    def __init__(self, request):
        self.request = request
        self.user = request.user

    def __resize(self, photo,resize_action_type=None):
        img = Image.open(photo.content_path)
        img_resized = img.resize(self.ACTION_TO_RESIZE['profile'])
        buffered = BytesIO()
        img_resized.save(buffered, format='png')
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64



    def filter_on_profile(self):
        """Генерация словаря по фильтру"""

        type_filter = self.request.GET.get('filter_value')
        photos = PhotoContent.objects.filter(user_id=self.request.user)
        if type_filter is None:
            return self.__create_response_dictionary(photos=photos)
        else:
            photos = PhotoContent.objects.filter(status=type_filter)
            return self.__create_response_dictionary(photos)

    def __create_response_dictionary(self, photos):
        response = {'data': []}
        for photo in photos:
            response['data'].append({'name': photo.name, 'media': self.__resize(photo=photo), 'created_data': photo.create_data,
                             'description': photo.description})
        return response
