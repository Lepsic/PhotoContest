import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from ..forms.upload_photo import UploadPhoto
from ..models import PhotoContent
from django.conf import settings
from ..service.photo_manager import PhotoManager


@login_required()
def base_account(request):
    """Базовая страница профиля"""

    context = {'username': request.user.username}

    return render(request, 'Account/base.html', context=context)


@login_required()
def a_filter_content(request):
    manager = PhotoManager(request=request)
    response = manager.filter_on_profile()
    return JsonResponse(response)


@login_required()
def upload_photo(request):
    """Загрузка фото на сервер"""
    if request.method == 'POST':
        form = UploadPhoto(request.POST, request.FILES)
        form.service_validate.set_data(request)
        if form.is_valid():
            form.service_validate.save_content()
            render(request, 'Account/upload.html')
        else:
            return render(request, 'Account/upload.html', {'form': form})
    else:
        form = UploadPhoto()
    return render(request, 'Account/upload.html', {'form': form})


@login_required()
def delete_photo(request):
    if request.method == 'DELETE':
        manager = PhotoManager(request)
        body = json.loads(request.body.decode('utf-8'))
        manager.delete_photo(body)
        return HttpResponse(status=200)


@login_required()
def change_photo():
    pass
