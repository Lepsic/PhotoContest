from django.urls import path
from ..views import moderation

urlpatterns = [
    path('publications/', moderation.get_photo_publication),
    path('publications/publish/', moderation.publication_photo),
    path('publications/publish/reject/', moderation.rejected_photo),
    path('rejects/', moderation.get_photo_rejected),
    path('rejects/cancel/', moderation.cancel_reject),
    path('changes/', moderation.get_change_photo),
    path('changes/approve/', moderation.approve_change),
    path('changes/cancel/', moderation.cancel_change),
    path('notification/', moderation.send_global_notification),

]
