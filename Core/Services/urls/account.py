from django.urls import path, include
from django.contrib.auth import views as auth_views

from ..views import account

urlpatterns = [
    path('profile/', account.base_account, name='account'),

]
