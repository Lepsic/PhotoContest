from django.urls import path
from ..views.profile import ProfileUploadPhoto, PhotoActions, ChangePhoto

urlpatterns = [
    path('upload/', ProfileUploadPhoto.as_view()),
    path('photoAction/', PhotoActions.as_view()),
    path('photoAction/Change/', ChangePhoto.as_view()),

]
