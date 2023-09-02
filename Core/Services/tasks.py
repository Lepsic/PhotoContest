from datetime import datetime, timedelta
from celery import shared_task
from .models import PhotoContent


@shared_task
def record_delete_photo(photo_id):
    photo = PhotoContent.objects.get(pk=photo_id)
    if photo.status == -1:
        photo.status = -100
        photo.save()


@shared_task
def schedule_delete_photo(photo_id):
    delete_time = datetime.now() + timedelta(seconds=10)
    record_delete_photo.apply_async(args=[photo_id], eta=delete_time)
