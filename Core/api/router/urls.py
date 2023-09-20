from django.urls import path, include


urlpatterns = [
     path('profile/', include('api.router.profile')),
     path('content/', include('api.router.mainpage')),

]