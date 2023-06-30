from ..models import PhotoContent
import base64
from PIL import Image
from io import BytesIO
from loguru import logger
from ..forms import upload_photo
from django.core.files import File as F


class PhotoManager:
    """Класс для взаимодействия с картинками"""

    ACTION_TO_RESIZE = {'profile': (220, 135)}

    def __init__(self, request):
        self.request = request
        self.user = request.user


    def __resize(self, photo, resize_action_type=None):
        img = Image.open(photo.content_path)
        img_resized = img.resize(self.ACTION_TO_RESIZE['profile'])
        buffered = BytesIO()
        img_resized.save(buffered, format='png')
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    def filter_on_profile(self):
        """Генерация словаря по фильтру"""

        type_filter = self.request.POST.get('filter_value')
        photos = PhotoContent.objects.filter(user_id=self.request.user)
        try:
            if type_filter != "None":
                type_filter = int(type_filter)
        except ValueError:
            logger.error("Не корректное значение filter_value из filter_content_profile.js")
            logger.info(type_filter)
        if type_filter == "None":
            return self.__create_response_dictionary(photos=photos)
        else:
            photos = PhotoContent.objects.filter(status=type_filter)
            return self.__create_response_dictionary(photos)

    def __create_response_dictionary(self, photos):
        """Создает словарь который отдает в запрос """
        response = {'data': []}
        for photo in photos:
            response['data'].append(
                {'name': photo.name, 'media': self.__resize(photo=photo), 'created_data': photo.create_data,
                 'description': photo.description, 'id': photo.pk})
        return response

    def delete_photo(self, body):
        photo = PhotoContent.objects.get(user_id=self.user, pk=body.get('id'))
        photo.status = -1
        photo.save()






