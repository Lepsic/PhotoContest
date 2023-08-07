from ..models import Comments
from ..models import Likes
from ..models import PhotoContent


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

