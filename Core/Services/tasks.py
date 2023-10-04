from datetime import datetime, timedelta

from celery import shared_task

from .models import PhotoContent, PhotoStateEnum


@shared_task
def record_delete_photo(photo_id):
    photo = PhotoContent.objects.get(pk=photo_id)
    if photo.state == PhotoStateEnum.ON_DELETE:
        photo.finish_delete()


@shared_task
def schedule_delete_photo(photo_id):
    delete_time = datetime.now() + timedelta(seconds=10)
    record_delete_photo.apply_async(args=[photo_id], eta=delete_time)


@shared_task
def record_reject_photo(photo_id):
    photo = PhotoContent.objects.get(pk=photo_id)
    if photo.state == PhotoStateEnum.REJECTED:
        photo.finish_reject()


@shared_task
def schedule_reject_photo(photo_id):
    reject_time = datetime.now() + timedelta(seconds=20)
    record_reject_photo.apply_async(args=[photo_id], eta=reject_time)
