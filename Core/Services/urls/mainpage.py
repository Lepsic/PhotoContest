from django.urls import path
from ..views import mainpage


urlpatterns = [
    path('', mainpage.main_page),
    path('content/photo/', mainpage.get_photo_content),
    path('content/like/', mainpage.likes_action),
    path('content/like/count/', mainpage.get_count_likes),


]