from django.db import models


class PhotoChange(models.Model):
    """Таблица изначальное фото - обновленное фото (для модерации)"""
    id = models.BigAutoField(primary_key=True)
    id_source = models.ForeignKey('PhotoContent', on_delete=models.DO_NOTHING, unique=True, related_name='source_photo')
    id_update = models.ForeignKey('PhotoContent', on_delete=models.DO_NOTHING, related_name='update_photo')
