from django.conf import settings
from django.apps import apps
from django.db.models import Count, Q
from Services.models.photo_content import PhotoContent, PhotoStateEnum
from Services.models.likes import Likes
from Services.models.comments import Comments
from Services.models.photo_change import PhotoChange
from rest_framework import status


class GetPhotoServiceBase:
    class RESIZE_ENUM:
        PROFILE = 'image_profile'
        ORIGINAL = 'image'
        MAIN_PAGES = 'image_main'

    class Meta:
        methods = ['_generate_photo_dictionary_on_change_stack', '_generate_photo_dictionary_on_publication_stack',
                   '_generate_photo_dictionary_on_rejected_stack', '_generate_photo_dictionary_on_photocard',
                   '_generate_photo_dictionary_on_main_page', '_generate_photo_dictionary_on_profile']

    def __init__(self, user=None):
        self._error = {}
        self._user = user
        self._response_status = None
        self._result = None

    @property
    def response_status(self):
        return self._response_status

    @property
    def errors(self):
        return self._error

    @property
    def result(self):
        return self._result

    def _resize(self, photo, action):
        try:
            return ''.join([settings.MEDIA_URL, getattr(photo, action).name])
        except AttributeError as error:
            self._error = error

    def execute(self, service_object_attributes, service_object_files):
        methods = service_object_attributes.get('methods')
        if methods in self.Meta.methods:
            if 'sort_type' in service_object_attributes:
                getattr(self, methods)(service_object_attributes.get('sort_type'))
            else:
                getattr(self, methods)()
            return self
        else:
            self._error.update()
            self._response_status = status.HTTP_400_BAD_REQUEST
            return self

    def _sort_main_pages(self, sort_type):
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
        else:
            self._error.update({'_sort_main_pages': 'Invalid filter value'})

    def _sort_profile_pages(self, sort_type):
        photos = PhotoContent.objects.filter(user_id=self._user)
        if sort_type == 'None':
            return photos
        if sort_type == '0':
            photos = PhotoContent.objects.filter(Q(state=PhotoStateEnum.WAIT_APPROVED) |
                                                 Q(state=PhotoStateEnum.ON_EDIT), user_id=self._user)
            return photos
        if sort_type == '1':
            photos = PhotoContent.objects.filter(state=PhotoStateEnum.APPROVED, user_id=self._user)
            return photos
        if sort_type == '-1':
            photos = PhotoContent.objects.filter(state=PhotoStateEnum.ON_DELETE, user_id=self._user)
            return photos
        else:
            self._error.update({'_sort_profile_pages': 'Invalid filter value'})
        return photos

    def _generate_photo_dictionary(self, action, photos, many=True):
        response = {'data': []}
        if many:
            for photo in photos:
                if photo.state != PhotoStateEnum.DONT_SHOW:
                    response['data'].append(
                        {'name': photo.name, 'media': self._resize(photo=photo, action=action),
                         'created_data': photo.create_data,
                         'description': photo.description, 'id': photo.pk,
                         'user': photo.user_id.id})
        else:
            photo = photos
            response['data'].append(response['data'].append(
                {'name': photo.name, 'media': self._resize(photo=photo, action=action),
                 'created_data': photo.create_data,
                 'description': photo.description, 'id': photo.pk,
                 'user': photo.user_id.id}))

        return response

    def _generate_photo_dictionary_on_profile(self, sort_type):
        photos = self._sort_profile_pages(sort_type)
        self._result = self._generate_photo_dictionary(action=self.RESIZE_ENUM.PROFILE, photos=photos)

    def _generate_photo_dictionary_on_main_page(self, sort_type):
        photos = self._sort_main_pages(sort_type)
        result = self._generate_photo_dictionary(self.RESIZE_ENUM.MAIN_PAGES, photos)
        if self._user.is_authenticated:
            for photo in result['data']:
                if Likes.objects.filter(photo_id=photo['id'], user_id=self._user).exists():
                    photo.update({'like_exist': 'True'})
                else:
                    photo.update({'like_exist': 'False'})
        else:
            for photo in result['data']:
                photo.update({'like_exist': 'False'})
        for photo in result['data']:
            photo.update({'like_count': str(Likes.objects.filter(photo_id=photo['id']).count())})
            photo.update({'comment_count': str(Comments.objects.filter(parent_id_image=photo['id']).count())})
        self._result = result

    def _generate_photo_dictionary_on_photocard(self, photo_id):
        photo = PhotoContent.objects.get(id=photo_id)
        result = self._generate_photo_dictionary(self.RESIZE_ENUM.ORIGINAL, photos=photo, many=False)
        if Likes.objects.filter(photo_id_id=photo_id, user_id=self._user).exists():
            result['data'][0].update({'like_exist': 'True'})
        else:
            result['data'][0].update({'like_exist': 'False'})
        result['data'][0].update({'like_count': str(Likes.objects.filter(photo_id=photo['id']).count())})
        result['data'][0].update({'comment_count': str(Comments.objects.filter(photo_id=photo['id']).count())})
        self._result = result

    def _generate_photo_dictionary_on_rejected_stack(self, **kwargs):
        photos = PhotoContent.objects.filter(state=PhotoStateEnum.REJECTED)
        self._result = self._generate_photo_dictionary(photos=photos, action=self.RESIZE_ENUM.PROFILE)

    def _generate_photo_dictionary_on_publication_stack(self, **kwargs):
        photos = PhotoContent.objects.filter(state=PhotoStateEnum.WAIT_APPROVED)
        self._result = self._generate_photo_dictionary(photos=photos, action=self.RESIZE_ENUM.PROFILE)

    def _generate_photo_dictionary_on_change_stack(self, **kwargs):
        update_photos = []
        changes = PhotoChange.objects.all()
        for change in changes:
            update_photos.append(change.id_update)
        response = self._generate_photo_dictionary(photos=update_photos, action=self.RESIZE_ENUM.PROFILE)
        for photo in response['data']:
            photo_source = PhotoChange.objects.get(id_update=photo['id']).id_source
            photo.update({'source_media': self._resize(photo_source, action=self.RESIZE_ENUM.PROFILE)})
        self._result = response
