import os

from ..models import PhotoContent, Likes
from .content_manager import ContentManager
import base64
from PIL import Image
from io import BytesIO
from loguru import logger
from ..forms import change_form
from ..models import PhotoChange
from .upload_photo import UploadManager
from django.db.models import Q, Count
from django.core.exceptions import FieldError



class PhotoManager:
    """Класс для взаимодействия с картинками"""

    ACTION_TO_RESIZE = {'profile_view': (220, 135),
                        'main_pages_view': (1280, 720),
                        }

    def __init__(self, request=None):
        self.ContentManager = ContentManager
        self.request = request
        if request is None:
            self.user = None
        else:
            self.user = request.user

    def update_data(self, requsest):
        """Метод для обновления данных по request"""
        self.request = requsest
        if self.user is None:
            self.user = requsest.user

    def generate_photo_dictionary_on_profile(self):
        """Генерация словаря по фильтру(для профиля)"""

        type_filter = self.request.POST.get('filter_value')
        photos = PhotoContent.objects.filter(user_id=self.user)
        try:
            if type_filter != "None":
                type_filter = int(type_filter)
        except ValueError:
            logger.error("Не корректное значение filter_value из filter_content_profile.js")
            logger.info(type_filter)
        if type_filter == "None":
            return self.__create_response_dictionary(photos=photos, resize_action_type='profile_view')
        else:
            if type_filter == 0:
                photos = PhotoContent.objects.filter(Q(status=type_filter) | Q(status=-2), user_id=self.user)
                return self.__create_response_dictionary(photos, resize_action_type='profile_view')

            photos = PhotoContent.objects.filter(status=type_filter, user_id=self.user)
            return self.__create_response_dictionary(photos, resize_action_type='profile_view')

    def generate_photo_dictionary_on_main_page(self):
        """Генерация словаря по фильтру для главной страницы"""
        sort_type = self.request.POST.get('sort_type')
        photos = self.__sort_photo_main_pages(sort_type)
        response = self.__create_response_dictionary(photos=photos, resize_action_type='main_pages_view')
        if self.request.user.is_authenticated:
            for photo in response['data']:
                if Likes.objects.filter(photo_id=photo['id'], user_id=self.request.user).exists():
                    photo.update({'like_exist': 'True'})
                else:
                    photo.update({'like_exist': 'False'})
        for photo in response['data']:
            like_count = Likes.objects.filter(photo_id=photo['id']).count()
            comment_count = self.ContentManager.get_count_comments_by_photo(photo_id=photo['id'])
            photo.update({'like_count': str(like_count)})
            photo.update({'comment_count': str(comment_count)})
            photo.update({'like_exist': 'False'})
        return response


    def _resize(self, photo, resize_action_type):
        img = Image.open(photo.content_path)
        img_resized = img.resize(self.ACTION_TO_RESIZE[resize_action_type])
        buffered = BytesIO()
        img_resized.save(buffered, format='png')
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    def __create_response_dictionary(self, photos, resize_action_type):
        """Создает словарь response с фотками"""
        response = {'data': []}
        for photo in photos:
            if photo.status != -100:
                response['data'].append(
                    {'name': photo.name, 'media': self._resize(photo=photo, resize_action_type=resize_action_type),
                     'created_data': photo.create_data,
                     'description': photo.description, 'id': photo.pk,
                     'user': photo.user_id.id})
        return response

    def delete_photo(self, body):
        """Фиктивное удаление(просто меняет статус)"""
        photo = PhotoContent.objects.get(user_id=self.user, pk=body.get('id'))
        photo.status = -1
        photo.save()

    def _all_delete_photo(self, photo):
        """Полное удаление фото из бд и из файловой системы"""
        os.remove(photo.content_path)
        photo.delete()

    def __sort_photo_main_pages(self, sort_type):
        if sort_type == 'create_data':
            photo = PhotoContent.objects.filter(status=1).order_by('create_data')
            return photo
        if sort_type == 'count_likes':
            photo = PhotoContent.objects.annotate(likes_count=Count('likes')).order_by('-like_count')
            return photo


class ChangePhotoManager(PhotoManager):
    def __init__(self):
        super().__init__()
        self.request = None
        self.id = None
        self.photo = None

    def set_request(self, request):
        self.request = request

    def set_id_change(self, id):
        self.id = id
        self.photo = PhotoContent.objects.get(pk=id)

    def creation_form(self):
        """Создание исходной формы по данным бд"""
        photo = self.photo
        file = ''.join(['data:image/png;base64,',
                        PhotoManager._resize(self, photo=photo, resize_action_type='profile_view')])
        initial = {'name': photo.name, 'description': photo.description}
        form = change_form.ChangePhoto(initial=initial)
        return {'form': form, 'file': file}

    def change_form(self):
        """Изменение фото"""
        form_update = change_form.ChangePhoto(self.request.POST, self.request.FILES)

        if form_update.is_valid():
            """Проверка на валидность формы"""
            source_dict = {'name': self.photo.name, 'description': self.photo.description}
            update_dict = {'name': form_update.cleaned_data['name'],
                           'description': form_update.cleaned_data['description']}
            if form_update.cleaned_data['media'] is None:
                """Если идет не идет редактированиее фото"""
                if source_dict != update_dict:
                    self.photo.name = update_dict['name']
                    self.photo.description = update_dict['description']
                    self.photo.save()
            else:
                """Если идет редактирование фото, то создается новая"""
                upload = UploadManager()
                upload.set_data(self.request)
                photo_created = upload.save_content(returned=True)
                change = PhotoChange(id_source=self.photo, id_update=photo_created)
                try:
                    change.save()
                except Exception:
                    if PhotoChange.objects.get(id_source=self.photo):
                        change = PhotoChange.objects.get(id_source=self.photo)

                        legacy_update_photo = change.id_update
                        change.id_update = photo_created
                        change.save()
                        self._all_delete_photo(legacy_update_photo)
                photo_created.status = -100
                photo_created.save()

    def __create_dictionary_for_save_form(self, form):
        """Создание словаря для сохранения фотки в бд"""
        user = self.user
        k_values = {'user_id': user, 'name': form.cleaned_data['name'], 'description': form.cleaned_data['description']}
        return k_values
