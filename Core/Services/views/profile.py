import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from ..forms.change_form import ChangePhoto
from ..forms.upload_photo_form import UploadPhoto
from Services.service.photo.upload_photo_form_service import UploadPhotoService
from ..models import PhotoContent
from ..service.photo_manager import ChangePhotoManager, PhotoManager
from Services.service.photo.get import GetPhotoServiceBase
from api.utils.service_outcome import ServiceOutcome
from Services.service.photo.change_photo_service import ChangePhotoService


login_url = '/authentication/login/'


@login_required(login_url=login_url)
def base_account(request):
    """Базовая страница профиля"""
    if not request.user.is_authenticated:
        return redirect('/authentication/login/?next=/profile/')
    context = {'username': request.user.username}

    return render(request, 'Account/base.html', context=context)


@login_required(login_url=login_url)
def a_filter_content(request):
    outcome = ServiceOutcome(GetPhotoServiceBase(user=request.user),
                              {'methods': '_generate_photo_dictionary_on_profile',
                               'sort_type': request.POST.get('filter_value')})
    return JsonResponse(outcome.result)


@login_required(login_url=login_url)
def upload_photo(request):
    """Загрузка фото на сервер"""
    if request.method == 'POST':
        service = UploadPhotoService(request.POST, request.FILES, user=request.user)
        if service.is_valid():
            service.process()
            return redirect('profile')
        else:
            return render(request, 'Account/upload.html', {'form': service})
    else:
        service = UploadPhotoService()
    return render(request, 'Account/upload.html', {'form': service})


@login_required(login_url=login_url)
def delete_photo(request):
    if request.method == 'DELETE':
        manager = PhotoManager(request)
        body = json.loads(request.body.decode('utf-8'))
        manager.delete_photo(body)
        return HttpResponse(status=200)


class ChangePhotoView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    @method_decorator(login_required(login_url=login_url))
    def get(self, request, id):
        service = ChangePhotoService(photo_id=id)
        return render(request, 'Account/change.html', context={'form_source': service,
                                                               'photo': service.base_photo_image_profile})

    @method_decorator(login_required(login_url=login_url))
    def post(self, request, id):
        service = ChangePhotoService(request.POST, request.FILES, photo_id=id, user=request.user)
        if service.is_valid():
            service.process()
            return redirect('profile')
        else:
            return render(request, 'Account/change.html', {'form': service})


@login_required(login_url=login_url)
def cancel_delete(request):
    photo_id = json.loads(request.body.decode('UTF-8')).get('id')
    user = request.user
    photo = PhotoContent.objects.get(pk=photo_id)
    if photo.user_id == user:
        photo.cancel_delete()
        return HttpResponse(request, status=200)
    else:
        from loguru import logger
        logger.error("Редактируемое фото не является фото, опубликовнное пользоваетлем,, отправившим запрос")
        return HttpResponse(request, status=404)


def get_user_data(request):
    user = request.user
    if user.is_authenticated:
        response = {"id": user.pk, 'username': user.username}
    else:
        response = {'NotAuthenticated'}
    return JsonResponse(response)






