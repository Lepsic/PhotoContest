from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from ..views import profile as view

urlpatterns = [
    path('profile/', view.base_account, name='profile'),
    path('profile/upload/', view.upload_photo, name='upload'),
    path('profile/filterUserPhoto/', view.a_filter_content),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
