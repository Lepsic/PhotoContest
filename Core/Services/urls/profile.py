import django.conf.global_settings
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from ..views import profile as view

urlpatterns = [
    path('', view.base_account, name='profile'),
    path('upload/', view.upload_photo, name='upload'),
    path('filterUserPhoto/', view.a_filter_content),
    path('delete/', view.delete_photo),
    path('change/<int:id>', view.ChangePhotoView.as_view(), name='change'),
    path('canceldelete/', view.cancel_delete, name='cancel delete'),
    path('user/data/get/', view.get_user_data),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
