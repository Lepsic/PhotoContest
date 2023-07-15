import os

from ..models import PhotoContent
import base64
from PIL import Image
from io import BytesIO
from loguru import logger
from ..forms import change_form
from ..models import PhotoChange
from .upload_photo import UploadManager
from django.db.models import Q


class PhotoManager:
    """Класс для взаимодействия с картинками"""

    ACTION_TO_RESIZE = {'profile': (220, 135)}

    def __init__(self, request=None):
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

    def _resize(self, photo, resize_action_type=None):
        img = Image.open(photo.content_path)
        img_resized = img.resize(self.ACTION_TO_RESIZE['profile'])
        buffered = BytesIO()
        img_resized.save(buffered, format='png')
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    def filter_on_profile(self):
        """Генерация словаря по фильтру"""

        type_filter = self.request.POST.get('filter_value')
        photos = PhotoContent.objects.filter(user_id=self.user)
        try:
            if type_filter != "None":
                type_filter = int(type_filter)
        except ValueError:
            logger.error("Не корректное значение filter_value из filter_content_profile.js")
            logger.info(type_filter)
        if type_filter == "None":
            return self.__create_response_dictionary_filtration(photos=photos)
        else:
            if type_filter == 0:
                photos = PhotoContent.objects.filter(Q(status=type_filter) | Q(status=-2), user_id=self.user)
                return self.__create_response_dictionary_filtration(photos)

            photos = PhotoContent.objects.filter(status=type_filter, user_id=self.user)
            return self.__create_response_dictionary_filtration(photos)

    def __create_response_dictionary_filtration(self, photos):
        """Создает словарь который отдает в запрос фильтрации"""
        response = {'data': []}
        for photo in photos:
            if photo.status != -100:
                response['data'].append(
                    {'name': photo.name, 'media': self._resize(photo=photo), 'created_data': photo.create_data,
                     'description': photo.description, 'id': photo.pk})
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
        print("удалилась по идее", type(photo))

    def create_change_photo(self):
        response = {}
        update_photo = PhotoContent.objects.filter(Q(user_id=self.user) | Q(status=-2))
        for photo in update_photo:
            response.update()


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
        file = ''.join(['data:image/png;base64,', PhotoManager._resize(self, photo=photo)])
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
                except:
                    if PhotoChange.objects.get(id_source=self.photo):
                        change = PhotoChange.objects.get(id_source=self.photo)

                        legacy_update_photo = change.id_update
                        print(legacy_update_photo)
                        change.id_update = photo_created
                        change.save()
                        self._all_delete_photo(legacy_update_photo)
                        print("Сюда не идем уже получается?")
                photo_created.status = -100
                photo_created.save()

    def __create_dictionary_for_save_form(self, form):
        """Создание словаря для сохранения фотки в бд"""
        user = self.user
        k_values = {'user_id': user, 'name': form.cleaned_data['name'], 'description': form.cleaned_data['description']}
        return k_values
