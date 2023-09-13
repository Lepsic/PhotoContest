import base64
import os
from io import BytesIO

from django.db.models import Count, Q
from loguru import logger
from PIL import Image

from ..forms import change_form
from ..models import Likes, PhotoChange, PhotoContent, PhotoStateEnum
from ..tasks import schedule_delete_photo
from .content_manager import ContentManager
from .upload_photo import UploadManager


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
            return self._create_response_dictionary(photos=photos, resize_action_type='profile_view')
        else:
            if type_filter == 0:
                photos = PhotoContent.objects.filter(Q(state=PhotoStateEnum.WAIT_APPROVED) |
                                                     Q(state=PhotoStateEnum.ON_EDIT), user_id=self.user)
                return self._create_response_dictionary(photos, resize_action_type='profile_view')
            if type_filter == 1:
                photos = PhotoContent.objects.filter(state=PhotoStateEnum.APPROVED, user_id=self.user)
                return self._create_response_dictionary(photos, resize_action_type='profile_view')
            if type_filter == -1:
                photos = PhotoContent.objects.filter(state=PhotoStateEnum.ON_DELETE, user_id=self.user)
                return self._create_response_dictionary(photos, resize_action_type='profile_view')
            photos = PhotoContent.objects.filter(state=type_filter, user_id=self.user)
            return self._create_response_dictionary(photos, resize_action_type='profile_view')

    def generate_photo_dictionary_on_publication_stack(self):
        """Генерация словаря фото"""
        photos = PhotoContent.objects.filter(state=PhotoStateEnum.WAIT_APPROVED)
        response = self._create_response_dictionary(photos, 'profile_view')
        return response
    def generate_photo_dictionary_on_rejected_stack(self):
        photos = PhotoContent.objects.filter(state=PhotoStateEnum.REJECTED)
        response = self._create_response_dictionary(photos, 'profile_view')
        return response

    def generate_photo_dictionary_on_main_page(self, photos=None):
        """Генерация словаря по фильтру для главной страницы"""
        if photos is None:
            sort_type = self.request.POST.get('sort_type')
            photos = self.__sort_photo_main_pages(sort_type)
        response = self._create_response_dictionary(photos=photos, resize_action_type='main_pages_view')
        if self.request.user.is_authenticated:
            for photo in response['data']:
                if Likes.objects.filter(photo_id=photo['id'], user_id=self.request.user).exists():
                    photo.update({'like_exist': 'True'})
                else:
                    photo.update({'like_exist': 'False'})
        else:
            for photo in response['data']:
                photo.update({'like_exist': 'False'})
        for photo in response['data']:
            like_count = Likes.objects.filter(photo_id=photo['id']).count()
            comment_count = self.ContentManager.get_count_comments_by_photo(photo_id=photo['id'])
            photo.update({'like_count': str(like_count)})
            photo.update({'comment_count': str(comment_count)})
        return response


    def _resize(self, photo, resize_action_type):
        img = Image.open(photo.content_path)
        img_resized = img.resize(self.ACTION_TO_RESIZE[resize_action_type])
        buffered = BytesIO()
        img_resized.save(buffered, format='png')
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    def _create_response_dictionary(self, photos, resize_action_type):
        """Создает словарь response с фотками"""
        response = {'data': []}
        for photo in photos:
            if photo.state != PhotoStateEnum.DONT_SHOW:
                response['data'].append(
                    {'name': photo.name, 'media': self._resize(photo=photo, resize_action_type=resize_action_type),
                     'created_data': photo.create_data,
                     'description': photo.description, 'id': photo.pk,
                     'user': photo.user_id.id})
        return response

    def delete_photo(self, body):
        """Фиктивное удаление(просто меняет статус)"""
        try:
            photo_id = body.get('id')
            photo = PhotoContent.objects.get(user_id=self.user, pk=body.get('id'))
            photo.initial_delete()
            schedule_delete_photo.delay(photo_id)
        except Exception as error:
            logger.error(error)

    def _all_delete_photo(self, photo):
        """Полное удаление фото из бд и из файловой системы"""
        os.remove(photo.content_path)
        photo.delete()

    def __sort_photo_main_pages(self, sort_type):
        if sort_type == 'create_data':
            photo = PhotoContent.objects.filter(state=PhotoStateEnum.APPROVED).order_by('create_data')
            return photo
        if sort_type == 'count_likes':
            photo = PhotoContent.objects.annotate(likes_count=Count('likes')).order_by('-likes_count').filter(
                state=PhotoStateEnum.APPROVED)
            return photo
        if sort_type == 'count_comments':
            photo = PhotoContent.objects.annotate(comments_count=Count('comments')).order_by('-comments_count').filter(
                state=PhotoStateEnum.APPROVED)
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
                photo_created.state = PhotoStateEnum.ON_EDIT
                photo_created.save()

    def __create_dictionary_for_save_form(self, form):
        """Создание словаря для сохранения фотки в бд"""
        user = self.user
        k_values = {'user_id': user, 'name': form.cleaned_data['name'], 'description': form.cleaned_data['description']}
        return k_values


    def get_change_photo(self):
        resize_type = 'profile_view'
        update_photos = []
        changes = PhotoChange.objects.all()
        for change in changes:
            update_photos.append(change.id_update)
        response = self._create_response_dictionary(update_photos, resize_type)
        for photo in response['data']:
            photo_source = PhotoChange.objects.get(id_update=photo['id']).id_source
            photo.update({'source_media': self._resize(photo_source, resize_type)})
        return response

