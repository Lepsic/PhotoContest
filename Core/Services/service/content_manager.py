import datetime

from loguru import logger

from ..models import Comments, Likes, PhotoContent
from .notification import comment_notification, like_notification


class ContentManager:

    @staticmethod
    def get_count_comments_by_photo(photo_id):
        """Подсчет количества комменатриев по id фото"""
        print(photo_id)
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
            like_notification(user_id=user, like_id=photo.name, action="DeletedLike", work_username=user.username,
                              like_count=str(ContentManager.get_count_likes_by_photo(photo_id)))
        else:
            like = Likes.objects.create(user_id=user, photo_id=photo)
            like.save()
            like_notification(user_id=user, like_id=like.photo_id.name, action="CreatedLike",
                              work_username=user.username,
                              like_count=str(ContentManager.get_count_likes_by_photo(photo_id)))

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
            photo = Comments.objects.get(id=created_data['parent_id']).parent_id_image
            comment = Comments.objects.create(user_id=created_data['user'], content=created_data['content'],
                                              parent_id_image_id=photo.id, entity_type=1,
                                              parent_id_comments_id=created_data['parent_id'],
                                              create_time=datetime.datetime.now())
        else:
            photo = PhotoContent.objects.get(id=created_data['image_id'])
            comment = Comments.objects.create(user_id=created_data['user'], content=created_data['content'],
                                              parent_id_image_id=photo.id, entity_type=0,
                                              create_time=datetime.datetime.now())
        comment.save()
        response = {'comment_id': comment.id}
        if comment.entity_type == 1:
            response.update({'comment_parent_id': comment.parent_id_comments.id})

        comment_notification(photo_id=photo.name, user_id=photo.user_id, action="CreatedComment",
                             work_username=created_data['user'].username,
                             comments_count=str(ContentManager.get_count_comments_by_photo(created_data['image_id'])))
        return response

    @staticmethod
    def delete_comment(comment_id, user):
        comment_id = int(comment_id)
        comment = Comments.objects.get(id=comment_id)
        if Comments.objects.filter(id=comment_id).exists():
            if Comments.objects.filter(entity_type=1, parent_id_comments_id=comment_id).exists():
                return False
            else:
                comment.delete()
                comment_notification(photo_id=comment.parent_id_image.name, user_id=comment.parent_id_image.user_id,
                                     action="DeletedComment",
                                     work_username=user.username,
                                     comments_count=str(
                                         ContentManager.get_count_comments_by_photo(comment.parent_id_image.id)))
                return True
        else:
            logger.error('Комментария с таким id не существует')

    @staticmethod
    def get_content_comment(comment_id):
        comment_id = int(comment_id)
        comment = Comments.objects.get(id=comment_id)
        return comment.content

    @staticmethod
    def edit_comment_content(comment_id, edit_text, user):
        comment_id = int(comment_id)
        print()
        comment = Comments.objects.get(id=comment_id)
        if edit_text != '':
            comment.content = edit_text
            comment.save()
            return True
        else:
            return ContentManager.delete_comment(comment_id, user)

    @staticmethod
    def search_photo(word):
        photos = PhotoContent.objects.filter(status=1)
        search_occurrences = []
        for photo in photos:
            search_list = [photo.user_id.username, photo.description, photo.name]
            for field in search_list:
                if word in field:
                    search_occurrences.append(photo)
                    break

        return search_occurrences
