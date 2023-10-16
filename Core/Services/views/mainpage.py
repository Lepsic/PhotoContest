from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from ..service.content_manager import ContentManager
from ..service.photo_manager import PhotoManager
from Services.service.photo.get import GetPhotoServiceBase
from Services.service.content.like.action import ActionLikeService
from Services.service.content.like.get import GetLikeService
from api.utils.service_outcome import ServiceOutcome


login_url = '/authentication/login/'


def main_page(request):
    context = {}
    if request.user.is_authenticated:
        context.update({'user': request.user})
    return render(request, 'mainpage/index.html', context=context)


def get_photo_content(request):
    outcome = ServiceOutcome(GetPhotoServiceBase(request.user),
                             {'methods': '_generate_photo_dictionary_on_main_page',
                              'sort_type': request.POST.get('sort_type')})
    return JsonResponse(outcome.result)


@login_required(login_url=login_url)
def likes_action(request):
    outcome = ServiceOutcome(ActionLikeService(user=request.user),
                             {'photo_id': request.POST.get('photo_id')})
    return JsonResponse(outcome.result)


def get_count_likes(request):
    """photo_id"""
    outcome = ServiceOutcome(GetLikeService(), {'photo_id': request.POST.get('photo_id')})
    return JsonResponse(outcome.result)


@login_required(login_url=login_url)
def post_comment(request):
    """Создание комментариев"""
    data = {'image_id': request.POST.get('image_id'), 'content': request.POST.get('content'), 'user': request.user,
            'parent_id_comment': request.POST.get('parent_id_comment'), 'parent_id': request.POST.get('parent_id')}
    content_manager = ContentManager
    response = content_manager.post_comment(data)
    return JsonResponse(response)


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

    if content_manager.delete_comment(comment_id, user=request.user):
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
    status = content_manager.edit_comment_content(comment_id, edit_text, user=request.user)
    if status:
        return JsonResponse({'username': request.user.username})
    else:
        return HttpResponseBadRequest('this comment cannot be changed to an empty str')


def search_on_photo(request):
    content_manager = ContentManager
    photo_manager = PhotoManager(request=request)
    photos = content_manager.search_photo(request.POST.get('searchData'))
    response = photo_manager.generate_photo_dictionary_on_main_page(photos=photos)
    return JsonResponse(response)


def generate_photo_page(request, image_id):
    pk = image_id
    photo_manager = PhotoManager(request)
    response = photo_manager.generate_photo_dictionary_on_photocard(pk)
    return JsonResponse(response)


def redirect_photo_page(request, image_id):
    return render(request, 'mainpage/photocard.html', context={'image_id': image_id})
