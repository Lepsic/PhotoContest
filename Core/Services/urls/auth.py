from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path


from ..views import auth

urlpatterns = [
    path('register/', auth.create_user, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),

]
