from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Services.service.Moderation import Moderation
from Services.service.photo_manager import ChangePhotoManager, PhotoManager
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from Services.service.moderation.changes import ChangesService
from Services.service.moderation.reject import RejectService
from Services.service.moderation.publiaction import PublicationService
from api.utils.service_outcome import ServiceOutcome
from Services.service.photo.get import GetPhotoServiceBase


class PublishView(APIView, Moderation, PhotoManager):
    """
    Класс для модерирования фотографий
    """

    def __init__(self):
        super().__init__()
        PhotoManager.__init__(self)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id фотографии'),
                'action': openapi.Schema(type=openapi.TYPE_STRING,
                                         description='Действие с фотографией (publish/reject)'),
            },
            required=['id', 'action'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            400: openapi.Response(description='Неверные параметры запроса'),
            401: openapi.Response(description='Пользователь не авторизован'),
        }
    )
    def post(self, request):
        """Публикация фотографий"""
        action = request.POST.get('action')
        user = request.user
        if user.is_superuser:
            if action == 'publish':
                outcome = ServiceOutcome(PublicationService(), {'post_id': request.POST.get('id')})
                return Response(outcome.response_status)
            elif action == 'reject':
                outcome = ServiceOutcome(RejectService(), {'methods': '_reject',
                                                           'post_id': request.POST.get('id')})
                return Response(status=outcome.response_status)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Запрос выполнен успешно', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Нзавние фото'),
                    'media': openapi.Schema(type=openapi.TYPE_STRING, description='фото в байтах'),
                    'created_data': openapi.Schema(type=openapi.TYPE_STRING, description='Дата создания'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id фото'),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
                }
            )),
            401: openapi.Response(description='Пользователь не авторизован'),
        }
    )
    def get(self, request):
        """
        Получает список фотографий в очереди на публикацию
        """
        if request.user.is_superuser:
            outcome = ServiceOutcome(GetPhotoServiceBase(),
                                     {'methods': '_generate_photo_dictionary_on_publication_stack'})
            return Response(outcome.result, status=outcome.response_status)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)


class RejectView(APIView, Moderation, PhotoManager):
    def __init__(self):
        super().__init__()
        PhotoManager.__init__(self)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Запрос выполнен успешно', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Нзавние фото'),
                    'media': openapi.Schema(type=openapi.TYPE_STRING, description='фото в байтах'),
                    'created_data': openapi.Schema(type=openapi.TYPE_STRING, description='Дата создания'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id фото'),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
                }
            )),
            401: openapi.Response(description='Пользователь не авторизован'),
        }
    )
    def get(self, request):
        """
        Возвращает список фотографий в очереди на отклонение
        """
        user = request.user
        if user.is_superuser:
            response = self.get_reject_stack()
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id фотографии'),
            },
            required=['id'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            401: openapi.Response(description='Пользователь не авторизован'),
        }
    )
    def post(self, request):
        user = request.user
        if user.is_superuser:
            # Moderation.cancel_reject(request.POST.get('id'))
            outcome = ServiceOutcome(RejectService(), {'methods': '_reject',
                                                       'post_id': request.POST.get('id')})
            return Response(status=outcome.response_status)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ChangeView(APIView, ChangePhotoManager, Moderation):
    def __init__(self):
        super().__init__()
        ChangePhotoManager.__init__(self)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Запрос выполнен успешно', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Нзавние фото'),
                    'media': openapi.Schema(type=openapi.TYPE_STRING, description='Обновленное фото в байтах'),
                    'created_data': openapi.Schema(type=openapi.TYPE_STRING, description='Дата создания'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description=
                            'id фото(на которое заменяется опубликованное)'),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
                    'source_media': openapi.Schema(type=openapi.TYPE_STRING, description='исходное фото в байтах')
                }
            )),
            401: openapi.Response(description='Пользователь не авторизован'),
        }
    )
    def get(self, request):
        """Получет фотки в очереди на изменение"""
        if request.user.is_superuser:
            outcome = ServiceOutcome(GetPhotoServiceBase(),
                                     {'methods': '_generate_photo_dictionary_on_change_stack'})
            return Response(outcome.result, status=outcome.response_status)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id фотографии'),
                'action': openapi.Schema(type=openapi.TYPE_STRING,
                                         description='Действие с фотографией (publish/reject)'),
            },
            required=['id', 'action'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            400: openapi.Response(description='Неверные параметры запроса'),
            401: openapi.Response(description='Пользователь не авторизован'),
        }
    )
    def post(self, request):
        """
        Постятся или отклоняются изменения
        id  - id update фотки
        action - (publish/reject)
        """
        user = request.user
        action = request.POST.get('action')
        pk = request.POST.get('id')
        if user.is_superuser:
            if action == 'publish':
                outcome = ServiceOutcome(ChangesService(),
                                         {'methods':  '_approve_changes',
                                          'change_id': request.POST.get('id')})
                return Response(status=outcome.response_status)
            elif action == 'reject':
                outcome = ServiceOutcome(ChangesService(), {'methods': '_reject_changes',
                                                            'change_id': request.POST.get('id')})
                return Response(status=outcome.response_status)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
