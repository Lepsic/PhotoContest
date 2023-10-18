from Services.service.Moderation import Moderation
from ..service.photo_manager import ChangePhotoManager
from loguru import logger
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from api.utils.service_outcome import ServiceOutcome
from Services.service.photo.get import GetPhotoServiceBase


@user_passes_test(lambda u: u.is_superuser)
def get_photo_publication(request):
    outcome = ServiceOutcome(GetPhotoServiceBase(),
                             {'methods': '_generate_photo_dictionary_on_publication_stack'})
    return JsonResponse(outcome.result)


@user_passes_test(lambda u: u.is_superuser)
def get_photo_rejected(request):
    outcome = ServiceOutcome(GetPhotoServiceBase(),
                             {'methods': '_generate_photo_dictionary_on_rejected_stack'})

    return JsonResponse(outcome.result)


@user_passes_test(lambda u: u.is_superuser)
def publication_photo(request):
    moderation = Moderation
    moderation.publication(request.POST.get('id'))
    return JsonResponse({})


@user_passes_test(lambda u: u.is_superuser)
def rejected_photo(request):
    moderation = Moderation
    moderation.reject(request.POST.get('id'))
    return JsonResponse({})


@user_passes_test(lambda u: u.is_superuser)
def cancel_reject(request):
    moderation = Moderation
    moderation.cancel_reject(request.POST.get('id'))
    return JsonResponse({})


@user_passes_test(lambda u: u.is_superuser)
def get_change_photo(request):
    outcome = ServiceOutcome(GetPhotoServiceBase(),
                             {'methods': '_generate_photo_dictionary_on_change_stack'})

    return JsonResponse(outcome.result)

@user_passes_test(lambda u: u.is_superuser)
def approve_change(request):
    manager = Moderation
    id_update = request.POST.get('id')
    manager.approve_public_change(id_update)
    return JsonResponse({})


@user_passes_test(lambda u: u.is_superuser)
def cancel_change(request):
    manager = Moderation
    id_update = request.POST.get('id')
    manager.cancel_public_change(id_update)
    return JsonResponse({})


@user_passes_test(lambda u: u.is_superuser)
def send_global_notification(request):
    text = request.POST.get('text')
    moderation = Moderation
    moderation.send_global_notification(text)
    return JsonResponse({})
