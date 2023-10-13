from ..models import PhotoContent, PhotoStateEnum
from ..models import PhotoChange
from ..service.photo_manager import PhotoManager
from ..tasks import schedule_reject_photo
from .notification import global_notification

class Moderation:
    @staticmethod
    def get_publication_stack():
        manager = PhotoManager()
        response = manager.generate_photo_dictionary_on_publication_stack()
        return response

    @staticmethod
    def get_reject_stack():
        manager = PhotoManager()
        response = manager.generate_photo_dictionary_on_rejected_stack()
        return response

    @staticmethod
    def publication(pk):
        pk = int(pk)
        photo = PhotoContent.objects.get(id=pk)
        photo.publish()

    @staticmethod
    def reject(pk):
        pk = int(pk)
        photo = PhotoContent.objects.get(id=pk)
        photo.initial_reject()
        schedule_reject_photo.delay(pk)

    @staticmethod
    def cancel_reject(pk):
        photo = PhotoContent.objects.get(id=pk)
        if photo.state == PhotoStateEnum.REJECTED:
            photo.cancel_reject()

    @staticmethod
    def approve_public_change(pk_update):
        change = PhotoChange.objects.get(id_update_id=pk_update)
        source_photo = change.id_source
        update_photo = change.id_update
        source_photo.name = update_photo.name
        source_photo.description = update_photo.description
        source_photo.create_data = update_photo.create_data
        source_photo.image = update_photo.image
        source_photo.image_main = update_photo.image_main
        source_photo.image_profile = update_photo.image_profile
        source_photo.save()
        update_photo.finish_edit()
        change.delete()

    @staticmethod
    def cancel_public_change(pk_update):
        change = PhotoChange.objects.get(id_update_id=pk_update)
        change.id_update.finish_edit()
        change.delete()

    @staticmethod
    def send_global_notification(text):
        global_notification(text)
