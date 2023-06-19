from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from ..forms.upload_photo import UploadPhoto
from ..models import photo_content
from ..service.upload_photo import UploadManager


@login_required()
def base_account(request):
    """Базовая страница профиля"""
    context = {'username': request.user.username}


    return render(request, 'Account/base.html', context=context)




@login_required()
def upload_photo(request):
    """Загрузка фото на сервер"""
    if request.method == 'POST':
        form = UploadPhoto(request.POST, request.FILES)
        if form.is_valid():
            photo_type = request.FILES.get('media').content_type
            print(type(photo_type))
            render(request, 'Account/upload.html')
        else:
            return render(request, 'Account/upload.html', {'form': form})
    else:
        form = UploadPhoto()
    return render(request, 'Account/upload.html', {'form': form})
