from ..models import Comments


class ContentManager:
    def get_count_comments_by_photo(self, photo_id):
        """Подсчет количества комменатриев по id фото"""
        comments = Comments.objects.filter(entity_type=0, photo_id=photo_id)

