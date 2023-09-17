from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Services.service.upload_photo import UploadManager
from Services.service.photo_manager import PhotoManager, ChangePhotoManager
import json

"""
    Для всего требуется авторизация 
    (в header передается session id)
"""

class ProfileUploadPhoto(APIView, UploadManager):
    """Загрузка фоток"""
    def __init__(self, **kwargs):
        super().__init__()
        UploadManager.__init__(self)

    def post(self, request):
        """
        Загрузка фото передается:
        name - название фотографии
        description - описание фотографии
        media - файл(img/png)
        """
        self.set_data(request=request)
        validate_result = self._validate_api()
        if validate_result is True:
            self.save_content()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': validate_result}, status=status.HTTP_400_BAD_REQUEST)


class PhotoActions(APIView, PhotoManager):
    """Активность фоток для главной страницы"""
    def __init__(self, **kwargs):
        super().__init__()
        PhotoManager.__init__(self)

    def post(self, request):
        """
        Получение фоток в профиле по типу сортировки(filter_value),
        Требуется авторизация(session_id передавать в header)
        1 - оупбликованные
        0 - в ождиании публикации
        -1 - на удалении
        None - все фотки(перечисленные тут)
        """
        self.update_data(self.request)
        response = self.generate_photo_dictionary_on_profile()
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Удаление фоток из профиля
        по id
        еще передается action если не передан или None, то происходит удаление,
        если передано знчаение cancelDelete то, произойдет отмена удаления
        """
        if request.POST.get('action') == 'delete':
            self.update_data(self.request)
            body = request.POST
            result = self.delete_photo(body)
            if result:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.POST.get('action') == 'cancel':
            status_response = self.cancel_delete()
            if status_response == 'Success':
                return Response(status=status.HTTP_200_OK)
            if status_response == 'Error':
                return Response(status=status.HTTP_400_BAD_REQUEST)








class ChangePhoto(APIView, ChangePhotoManager):
    """Класс для изменения фото"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ChangePhotoManager.__init__(self)

    def patch(self, request):
        """
        изменение фото
        id - id изменяемой фотографии
        name - название(может сопадать, если не совпадает, то будет изменено, передавать обязательно)
        description - описание фотографии(может сопадать, если не совпадает, то будет изменено, передавать обязательно)
        media - файл(jpg/png) Если передан, то будет поставлена в очереди на модерацию(не обязательный параметр)
        """
        self.set_request(request=request)
        self.change_request()
        return Response(status=status.HTTP_400_BAD_REQUEST)

