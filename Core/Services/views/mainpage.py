from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from ..service.photo_manager import PhotoManager
from ..service.content_manager import ContentManager
from django.http import HttpResponseBadRequest

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



def get_comment_by_photo(request):
    """Получение комментариев по id фото"""
    content_manager = ContentManager
    pk = request.POST.get('photoId')
    response = content_manager.get_comments_dictionary(pk)
    return JsonResponse(response)


@login_required(login_url=login_url)
def delete_comment(request):
    content_manager = ContentManager
    comment_id = request.POST.get('comment_id')

    if content_manager.delete_comment(comment_id):
        return JsonResponse({})
    else:
        return HttpResponseBadRequest('The comment is not available for deletion')


def get_content_comment(request):
    comment_id = request.POST.get('comment_id')
    content_manager = ContentManager
    content = content_manager.get_content_comment(comment_id)
    return JsonResponse({'commentContent': content})


@login_required(login_url=login_url)
def edit_content_comment(request):
    comment_id = request.POST.get('comment_id')
    edit_text = request.POST.get('editText')
    content_manager = ContentManager
    status = content_manager.edit_comment_content(comment_id, edit_text)
    if status:
        return JsonResponse({'username': request.user.username})
    else:
        return HttpResponseBadRequest('this comment cannot be changed to an empty str')
