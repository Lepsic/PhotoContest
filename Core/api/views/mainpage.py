from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Services.service.photo_manager import PhotoManager
from Services.service.content_manager import ContentManager
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Services.service.photo.get import GetPhotoServiceBase
from Services.service.photo.post import PostPhotoService
from Services.service.content.like.action import ActionLikeService
from Services.service.content.like.get import GetLikeService
from Services.service.content.comment.get import GetCommentService
from Services.service.content.comment.post import PostCommentService
from Services.service.content.comment.delete import DeleteCommentService
from Services.service.content.comment.update import UpdateCommentService
from api.utils.service_outcome import ServiceOutcome


class GetPhoto(APIView):
    """Получение и поиск опубликованных фотографий"""

    def __init__(self):
        super().__init__()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(type=openapi.TYPE_STRING, description='Возможные значения: "search", "get"'),
                'searchWord': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='Слово по которому будет проводиться поиск'),
                'sort_type': openapi.Schema(type=openapi.TYPE_STRING,
                                            description='Возможные значения: "count_likes", "count_comments", '
                                                        '"create_data"'),
            },
            required=['action'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Нзавние фото'),
                    'media': openapi.Schema(type=openapi.TYPE_STRING, description='фото в байтах'),
                    'created_data': openapi.Schema(type=openapi.TYPE_STRING, description='Дата создания'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id фото'),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
                    'like_exist': openapi.Schema(type=openapi.TYPE_STRING, description='Существует лайк или нет. '
                                                                                       'Принимает значение true/false'),
                    'like_count': openapi.Schema(type=openapi.TYPE_STRING, description='Количество лайков'),
                    'comment_count': openapi.Schema(type=openapi.TYPE_STRING, description='Количество комментариев')
                }
            )),
            400: openapi.Response(description='Неверные параметры запроса'),
        }
    )
    def post(self, request):
        """
        Передается action
        если action = search:

        в request нужно передать searchWord  (слово по которому будет
        проводиться поиск)

        если action = get:

        в request передать тип фильтра sort_type:
        По количеству лайков - count_likes
        По количеству комментов - count_comments
        По дате создание - create_data
        """
        if request.POST.get('action') == 'search':
            # search_word = request.POST.get('searchWord')
            # photos = ContentManager.search_photo(search_word)
            # response = self.generate_photo_dictionary_on_main_page(photos=photos)
            outcome = ServiceOutcome(GetPhotoServiceBase(request.user),
                                     {'methods': '_generate_photo_dictionary_on_search',
                                      'sort_type': request.POST.get('searchWord')})
            return Response(outcome.result, status=outcome.response_status)
        if request.POST.get('action') == 'get':
            # self.update_data(request)
            # response = self.generate_photo_dictionary_on_main_page()
            outcome = ServiceOutcome(GetPhotoServiceBase(request.user),
                                     {'methods': '_generate_photo_dictionary_on_main_page',
                                      'sort_type': request.POST.get('sort_type')})
            return Response(outcome.result, status=outcome.response_status)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('value_id', openapi.IN_PATH, description='Id фотографии', type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(description='Запрос выполнен успешно', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Нзавние фото'),
                    'media': openapi.Schema(type=openapi.TYPE_STRING, description='фото в байтах'),
                    'created_data': openapi.Schema(type=openapi.TYPE_STRING, description='Дата создания'),
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id фото'),
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
                    'like_exist': openapi.Schema(type=openapi.TYPE_STRING, description='Существует лайк или нет. '
                                                                                       'Принимает значение true/false'),
                    'like_count': openapi.Schema(type=openapi.TYPE_STRING, description='Количество лайков'),
                    'comment_count': openapi.Schema(type=openapi.TYPE_STRING, description='Количество комментариев')
                }
            )),
        }
    )
    def get(self, request, value_id):
        # self.update_data(request)
        # response = self.generate_photo_dictionary_on_photocard(value_id)
        outcome = ServiceOutcome(GetPhotoServiceBase(request.user),
                                 {'methods': '_generate_photo_dictionary_on_photocard',
                                  'sort_type': value_id})

        return Response(outcome.result, status=outcome.response_status)


class LikeAction(APIView):
    """Функционал лайков"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'photo_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id фотографии'),
            },
            required=['photo_id'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            400: openapi.Response(description='Неверные параметры запроса'),
        }
    )
    def post(self, request):
        """
        Метод для создание/удаление(Если лайка нет, то создастся, если есть,
        то удалится)
        передается photo_id
        """
        user = request.user
        if user.is_authenticated:
            # photo_id = request.POST.get('photo_id')
            # ContentManager.likes_action(photo_id, user)
            outcome = ServiceOutcome(LikeAction(user), {'photo_id': request.POST.get('photo_id')})
            return Response(status=outcome.response_status)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentAction(APIView):
    """Функционал комментариев"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id фотографии'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Текст комментария'),
                'parent_id_comment': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                    description='Флаг ответа на комментарий'),
                'parent_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                            description='Id комментария на который отвечает данный комментарий (только в случае если комментарий является ответом)'),
            },
            required=['image_id', 'content', 'parent_id_comment'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            400: openapi.Response(description='Неверные параметры запроса'),
        }
    )
    def post(self, request):
        """
        Пост коммента или ответ на него
        Если постится ответ, то 'parent_id_comment = true',
        Если постится просто коммент, то 'parent_id_comment = false'
        обязательно передается user(session в header)
        parent_id_image_id - id фото
        content - текст комментария
        parent_id_comments_id - id комментария на который отвечает данный комментарий(только в случе
        если комментарий является ответом)

        """
        user = request.user
        if user.is_authenticated:
            data = {'image_id': request.POST.get('image_id'), 'content': request.POST.get('content'),
                    'user': request.user,
                    'parent_id_comment': request.POST.get('parent_id_comment'),
                    'parent_id': request.POST.get('parent_id')}
            outcome = ServiceOutcome(PostCommentService(request.user), data)
            return Response(outcome.result, status=outcome.response_status)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'comment_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id комментария'),
            },
            required=['comment_id'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            409: openapi.Response(description='Конфликт при удалении комментария'),
        }
    )
    def delete(self, request):
        """
        Удаление комментариев
        передается
        id = comment_id
        """
        comment_id = request.POST.get('comment_id')
        outcome = ServiceOutcome(DeleteCommentService(request.user), request.POST.get('comment_id'))
        return Response(outcome.result, status=outcome.response_status)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'comment_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Id комментария'),
                'editText': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='Текст, на который нужно заменить комментарий'),
            },
            required=['comment_id', 'editText'],
        ),
        responses={
            200: openapi.Response(description='Запрос выполнен успешно'),
            409: openapi.Response(description='Конфликт при изменении комментария')
        })
    def patch(self, request):
        """
        Изменение комментариев
        передается только
        comment_id - id комментария
        editText - текст, на которой нужно заменить коммент
        """
        # comment_id = request.POST.get('comment_id')
        # edit_text = request.POST.get('editText')
        outcome = ServiceOutcome(UpdateCommentService(request.user),
                                 {'comment_id': request.POST.get('comment_id'),
                                  'edit_text': request.POST.get('editText')})
        return Response(outcome.result, status=outcome.response_status)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('value_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='Id фотографии'),
        ],
        responses={
            200: openapi.Response(description='Запрос выполнен успешно', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_STRING, description='id комментария'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользака'),
                    'content': openapi.Schema(type=openapi.TYPE_STRING, description='Текст комментария'),
                    'count_child_comments': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество ответов '
                                                                                                  'на комментарий'),
                    'child_comment': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Является дочерним '
                                                                                           'комментом или нет'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опубликовавшего пользователя')
                }
            )),
        }
    )
    def get(self, request, value_id):
        """
        Передается id фото(value_id)
        Возвращает список комментариев словарем
        """
        outcome = ServiceOutcome(GetCommentService(), {'photo_id': value_id})
        return Response(outcome.result, status=outcome.response_status)
