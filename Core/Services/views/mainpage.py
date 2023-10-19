from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from Services.service.photo.get import GetPhotoServiceBase
from Services.service.content.like.action import ActionLikeService
from Services.service.content.like.get import GetLikeService
from Services.service.content.comment.get import GetCommentService
from Services.service.content.comment.post import PostCommentService
from Services.service.content.comment.delete import DeleteCommentService
from Services.service.content.comment.update import UpdateCommentService
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
    data = {'image_id': request.POST.get('image_id'), 'content': request.POST.get('content'),
            'parent_id_comment': request.POST.get('parent_id_comment'), 'parent_id': request.POST.get('parent_id')}
    outcome = ServiceOutcome(PostCommentService(request.user), data)
    return JsonResponse(outcome.result)


def get_comment_by_photo(request):
    """Получение комментариев по id фото"""
    outcome = ServiceOutcome(GetCommentService(), {'photo_id': request.POST.get('photoId')})
    return JsonResponse(outcome.result)


@login_required(login_url=login_url)
def delete_comment(request):
    outcome = ServiceOutcome(DeleteCommentService(request.user), request.POST.get('comment_id'))
    if outcome.errors:
        return JsonResponse(outcome.result)
    else:
        return HttpResponseBadRequest()


def get_content_comment(request):
    outcome = ServiceOutcome(GetCommentService(), {'comment_id': request.POST.get('comment_id')})
    return JsonResponse(outcome.result)


@login_required(login_url=login_url)
def edit_content_comment(request):
    outcome = ServiceOutcome(UpdateCommentService(request.user),
                             {'comment_id': request.POST.get('comment_id'),
                              'edit_text': request.POST.get('editText')})
    if outcome.errors:
        return JsonResponse({'username': request.user.username})
    else:
        return HttpResponseBadRequest('Does not Update Comments')


def search_on_photo(request):
    outcome = ServiceOutcome(GetPhotoServiceBase(user=request.user),
                             {'methods': '_generate_photo_dictionary_on_search',
                              'sort_type': request.POST.get('searchData')})
    return JsonResponse(outcome.result)


def generate_photo_page(request, image_id):
    outcome = ServiceOutcome(GetPhotoServiceBase(user=request.user),
                             {'methods': '_generate_photo_dictionary_on_photocard',
                              'sort_type': image_id})
    return JsonResponse(outcome.result)


def redirect_photo_page(request, image_id):
    return render(request, 'mainpage/photocard.html', context={'image_id': image_id})
