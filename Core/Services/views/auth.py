import http

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from ..forms import auth_forms


def create_user(request):
    if request.method == 'POST':
        form = auth_forms.UserCreationsForm(request.POST)
        if form.is_valid():
            form.service.SaveUser()
            return redirect('login')
        else:
            return render(request, 'auth/create.html', {'form':form})
    else:
        form = auth_forms.UserCreationsForm
        return render(request, 'auth/create.html', {'form': form})