from django.urls import path
from ..views import mainpage

urlpatterns = [
    path('', mainpage.main_page),
    path('content/photo/', mainpage.get_photo_content),
    path('content/like/', mainpage.likes_action),
    path('content/like/count/', mainpage.get_count_likes),
    path('content/comment/post/', mainpage.post_comment),
    path('content/comment/get/', mainpage.get_comment_by_photo),
    path('content/comment/delete/', mainpage.delete_comment),
    path('content/comment/text/', mainpage.get_content_comment),
    path('content/comment/edit/', mainpage.edit_content_comment)

]
