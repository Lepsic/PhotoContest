from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Services.service.upload_photo import UploadManager
from Services.service.photo_manager import PhotoManager, ChangePhotoManager
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

"""
    Для всего требуется авторизация 
    (в header передается session id)
"""


class ProfileUploadPhoto(APIView, UploadManager):
    """Загрузка фоток"""

    def __init__(self, **kwargs):
        super().__init__()
        UploadManager.__init__(self)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название фотографии'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание фотографии'),
                'media': openapi.Schema(type=openapi.TYPE_FILE, description='Файл фотографии (img/png)'),
            },
            required=['name', 'media'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            400: openapi.Response(description='Неверные параметры запроса', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Описание ошибки')
                }
            )),
        }
    )
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'filter_value': openapi.Schema(type=openapi.TYPE_STRING, description='Тип сортировки фотографий'),
            },
            required=['filter_value']
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Нзавние фото'),
                    'media': openapi.Schema(type=openapi.TYPE_STRING, description='фото в байтах'),
                    'created_data': openapi.Schema(type=openapi.TYPE_STRING, description='Дата создания'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание фотографии'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id фото'),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
                })),
        }
    )
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID фотографии'),
                'action': openapi.Schema(type=openapi.TYPE_STRING, description='Действие'),
            },
            required=['id'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            400: openapi.Response(description='Неверные параметры запроса'),
        }
    )
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID изменяемой фотографии'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название фотографии'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание фотографии'),
                'media': openapi.Schema(type=openapi.TYPE_FILE, description='Файл (jpg/png)'),
            },
            required=['id', 'name', 'description'],
            responses={
                200: openapi.Response(description='Запрос выполнен успешно')
            }
        ),

    )
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
        return Response(status=status.HTTP_200_OK)
