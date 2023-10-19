from django.contrib.auth.views import LogoutView as Logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from allauth.account.views import SignupView

from ..forms import auth_forms
from ..forms import SocialForm
from Services.service.auth.service_registration import RegistrationUserService


def create_user(request):
    if request.method == 'POST':
        service = RegistrationUserService(request.POST)
        if service.is_valid():
            service.process()
            return redirect('login')
        else:
            return render(request, 'auth/create.html', {'form': service})
    else:
        service = RegistrationUserService
        return render(request, 'auth/create.html', {'form': service})


class LogoutView(Logout):
    next_page = reverse_lazy('login')
