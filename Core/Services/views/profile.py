import json
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from ..forms.upload_photo_form import UploadPhoto
from ..models import PhotoContent
from django.conf import settings
from django.views import View
from ..service.photo_manager import PhotoManager, ChangePhotoManager
from ..forms.change_form import ChangePhoto

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
    manager = PhotoManager(request=request)
    response = manager.generate_phtoto_dictionary_on_profile()
    return JsonResponse(response)


@login_required(login_url=login_url)
def upload_photo(request):
    """Загрузка фото на сервер"""
    if request.method == 'POST':
        form = UploadPhoto(request.POST, request.FILES)
        form.service_validate.set_data(request)
        if form.is_valid():
            form.service_validate.save_content()
            return redirect('profile')
        else:
            return render(request, 'Account/upload.html', {'form': form})
    else:
        form = UploadPhoto()
    return render(request, 'Account/upload.html', {'form': form})


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
        self.manager = ChangePhotoManager()

    @method_decorator(login_required(login_url=login_url))
    def get(self, request, id):
        self.manager.set_request(request)
        self.manager.set_id_change(id)
        data = self.manager.creation_form()
        return render(request, 'Account/change.html', context={'form_source': data['form'],
                                                               'photo': data['file']})

    @method_decorator(login_required(login_url=login_url))
    def post(self, request, id):
        self.manager.set_id_change(id)
        self.manager.set_request(request)
        form = ChangePhoto(request.POST, request.FILES)
        if form.is_valid():
            self.manager.change_form()
            return redirect('profile')
        else:
            return render(request, 'Account/change.html', {'form': form})


@login_required(login_url=login_url)
def cancel_delete(request):
    photo_id = json.loads(request.body.decode('UTF-8')).get('id')
    user = request.user
    photo = PhotoContent.objects.get(pk=photo_id)
    if photo.user_id == user:
        photo.status = 1
        photo.save()
        return HttpResponse(request, status=200)
    else:
        from loguru import logger
        logger.error("Редактируемое фото не является фото, опубликовнное пользоваетлем,, отправившим запрос")
        return HttpResponse(request, status=404)
