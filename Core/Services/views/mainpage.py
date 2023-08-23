from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from ..service.photo_manager import PhotoManager
from ..service.content_manager import ContentManager

login_url = '/authentication/login/'


def main_page(request):
    return render(request, 'mainpage/index.html')


def get_photo_content(request):
    manager = PhotoManager(request)
    response = manager.generate_photo_dictionary_on_main_page()
    return JsonResponse(response)


@login_required(login_url=login_url)
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


@login_required(login_url=login_url)
def post_comment(request):
    """Создание комментариев"""
    data = {'image_id': request.POST.get('image_id'), 'content': request.POST.get('content'), 'user': request.user,
            'parent_id_comment': request.POST.get('parent_id_comment'), 'parent_id': request.POST.get('parent_id')}
    content_manager = ContentManager
    content_manager.post_comment(data)
    return HttpResponse(status=200)



@login_required(login_url=login_url)
def get_comment_by_photo(request):
    """Получение комментариев по id фото"""
    content_manager = ContentManager
    pk = request.POST.get('photoId')
    response = content_manager.get_comments_dictionary(pk)
    return JsonResponse(response)
