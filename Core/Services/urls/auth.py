from django.urls import path, include
from django.contrib.auth import views as auth_views

from ..views import auth

urlpatterns = [
    path('register/', auth.create_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(), name='logout')


]
