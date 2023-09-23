from django.urls import path
from ..views.mainpage import *

urlpatterns = [
    path('photo/', GetPhoto.as_view()),
    path('like/', LikeAction.as_view()),
    path('comment/', CommentAction.as_view()),
    path('photo/<int:value_id>/', GetPhoto.as_view()),
    path('comment/<int:value_id>/', CommentAction.as_view())


]
