from django.urls import path, include
from django.contrib.auth import views as auth_views

from ..views import profile as view

urlpatterns = [
    path('profile/', view.base_account, name='profile'),
    path('profile/upload/', view.upload_photo, name='upload'),
]
