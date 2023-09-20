from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Services.service.photo_manager import PhotoManager
from Services.service.content_manager import ContentManager


class GetPhoto(APIView, PhotoManager, ContentManager):
    """Получение и поиск опубликованных фотографий"""
    def __init__(self):
        super().__init__()
        PhotoManager.__init__(self)

    def post(self, request):
        """
        Передается action
        если action = search:

        в request нужно передать searchWord и слово по которому будет
        проводиться поиск

        если action = get:

        в request передать тип фильтра sort_type:
        По количеству лайков - count_likes
        По количеству комментов - count_comments
        По дате создание - create_data
        """
        if request.POST.get('action') == 'search':
            search_word = request.POST.get('searchWord')
            photos = ContentManager.search_photo(search_word)
            response = self.generate_photo_dictionary_on_main_page(photos=photos)
            return Response(response, status=status.HTTP_200_OK)
        if request.POST.get('action') == 'get':
            self.update_data(request)
            response = self.generate_photo_dictionary_on_main_page()
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, value_id):
        self.update_data(request)
        response = self.generate_photo_dictionary_on_photocard(value_id)
        return Response(response, status=status.HTTP_200_OK)



class LikeAction(APIView):
    """Функционал лайков"""
    def post(self, request):
        """
        Метод для создание/удаление(Если лайка нет, то создастся, если есть,
        то удалится)
        передается photo_id
        """
        user = request.user
        if user.is_authenticated:
            photo_id = request.POST.get('photo_id')
            ContentManager.likes_action(photo_id, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class CommentAction(APIView):
    """Функционал комментариев"""
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
            response = ContentManager.post_comment(data)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Удаление комментариев
        передается
        id = comment_id
        """
        comment_id = request.POST.get('comment_id')
        if ContentManager.delete_comment(comment_id, request.user):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

    def patch(self, request):
        """
        Изменение комментариев
        передается только
        comment_id - id комментария
        editText - текст, на которой нужно заменить коммент
        """
        comment_id = request.POST.get('comment_id')
        edit_text = request.POST.get('editText')
        state = ContentManager.edit_comment_content(comment_id, edit_text, request.user)
        if state:
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_409_CONFLICT)


    def get(self, request, value_id):
        """
        Передается id фото(value_id)
        Возвращает список комментариев словарем
        """
        response = ContentManager.get_comments_dictionary(value_id)
        return Response(response, status=status.HTTP_200_OK)
