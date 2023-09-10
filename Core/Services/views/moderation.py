from ..service import moderation
from loguru import logger
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def my_view(request):
    "Пример проверки на то является ли пользак суперюзером"
    pass
