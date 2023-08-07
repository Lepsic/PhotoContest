from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from ..service.photo_manager import PhotoManager
from ..service.content_manager import ContentManager


def main_page(request):
    return render(request, 'mainpage/index.html')


def get_photo_content(request):
    manager = PhotoManager(request)
    response = manager.generate_photo_dictionary_on_main_page()
    return JsonResponse(response)


@login_required()
def likes_action(request):
    content_manager = ContentManager
    user = request.user
    photo_id = request.POST.get('photo_id')
    content_manager.likes_action(user=user, photo_id=photo_id)
    response = {"count_likes": str(content_manager.get_count_likes_by_photo(request.POST.get('photo_id')))}
    return JsonResponse(response)


def get_count_likes(request):
    content_manager = ContentManager
    response = {"count_likes": str(content_manager.get_count_likes_by_photo(request.POST.get('photo_id')))}
    return JsonResponse(response)
