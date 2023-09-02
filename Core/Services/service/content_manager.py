import datetime

from ..models import Comments
from ..models import Likes
from ..models import PhotoContent
from loguru import logger


class ContentManager:

    @staticmethod
    def get_count_comments_by_photo(photo_id):
        """Подсчет количества комменатриев по id фото"""
        return Comments.objects.filter(parent_id_image=photo_id).count()

    @staticmethod
    def get_count_likes_by_photo(photo_id):
        """Подсчет количества лайков по id фото"""
        return Likes.objects.filter(photo_id=photo_id).count()

    @staticmethod
    def likes_action(photo_id, user):
        """Обработка нажатия на кнопку лайка"""
        photo = PhotoContent.objects.get(pk=photo_id)
        like = Likes.objects.filter(photo_id=photo, user_id=user)
        if like.exists():
            like.delete()


        else:
            like = Likes.objects.create(user_id=user, photo_id=photo)
            like.save()

    @staticmethod
    def __get_child_comments(comment):
        c_comments = Comments.objects.filter(entity_type=1, parent_id_comments=comment)
        if c_comments.count == 0:
            return False
        return c_comments

    @staticmethod
    def get_comments_dictionary(photo_id):
        """получение комментариев по id фото"""
        comments = Comments.objects.filter(parent_id_image_id=photo_id)
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
        return response

    @staticmethod
    def post_comment(created_data):

        if created_data['parent_id_comment'] == 'true':
            comment = Comments.objects.create(user_id=created_data['user'], content=created_data['content'],
                                              parent_id_image_id=created_data['image_id'], entity_type=1,
                                              parent_id_comments_id=created_data['parent_id'],
                                              create_time=datetime.datetime.now())
        else:
            comment = Comments.objects.create(user_id=created_data['user'], content=created_data['content'],
                                              parent_id_image_id=created_data['image_id'], entity_type=0,
                                              create_time=datetime.datetime.now())
        comment.save()

    @staticmethod
    def delete_comment(comment_id):
        comment_id = int(comment_id)
        comment = Comments.objects.filter(id=comment_id)
        if Comments.objects.filter(id=comment_id).exists():
            if Comments.objects.filter(entity_type=1, parent_id_comments_id=comment_id).exists():
                return False
            else:
                print('этот блок выполняется')
                comment.delete()
                return True
        else:
            logger.error('Комментария с таким id не существует')

    @staticmethod
    def get_content_comment(comment_id):
        comment_id = int(comment_id)
        comment = Comments.objects.get(id=comment_id)
        return comment.content

    @staticmethod
    def edit_comment_content(comment_id, edit_text):
        comment_id = int(comment_id)
        print()
        comment = Comments.objects.get(id=comment_id)
        if edit_text != '':
            comment.content = edit_text
            comment.save()
            return True
        else:
            return ContentManager.delete_comment(comment_id)
