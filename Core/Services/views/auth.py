
from django.contrib.auth.views import LogoutView as Logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


from ..forms import auth_forms


def create_user(request):
    if request.method == 'POST':
        form = auth_forms.UserCreationsForm(request.POST)
        if form.is_valid():
            form.service.SaveUser()
            return redirect('login')
        else:
            return render(request, 'auth/create.html', {'form': form})
    else:
        form = auth_forms.UserCreationsForm
        return render(request, 'auth/create.html', {'form': form})


class LogoutView(Logout):
    next_page = reverse_lazy('login')

def callback(request):
    pass
