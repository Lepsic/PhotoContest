from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse


@login_required()
def base_account(request):
    user_id = request.user.pk
    context = {'username': request.user.pk}

    return render(request, 'Account/base.html', context=context)
