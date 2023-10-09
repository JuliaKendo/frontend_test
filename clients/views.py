import json

from django.http import JsonResponse
from django.shortcuts import (
    render, redirect
)
from contextlib import suppress

from .login import Login, AuthenticationError

from .forms import (
    RegForm,
    LoginForm,
    ChangePassForm
)
from .models import (
    Client,
    RegistrationOrder,
)


def login(request):
    if request.method != 'POST':
        form = LoginForm()
        return render(request, 'forms/auth.html', {'form': form})
    
    login = Login(request)
    form = LoginForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.as_json()})
    
    with suppress(AuthenticationError):
        login.auth(**form.cleaned_data)
        return redirect('start_page')

    return JsonResponse(
        {'errors': json.dumps(
            {'login': [{'message': 'Неверный логин или пароль'},]}
        )}
    )


def register(request):
    if request.method != 'POST':
        form = RegForm()
        return render(request, 'forms/sign-in.html', {'form': form})

    form = RegForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.as_json()})
        
    RegistrationOrder.objects.get_or_create(
        inn=form.cleaned_data['inn'],
        defaults=form.cleaned_data,
    )
    return redirect('start_page')


def register_confirm(request):
    return redirect('start_page')


def logout(request):
    login = Login(request)
    login.unauth()
    return redirect('start_page')


def change_password(request):
    if request.method != 'POST':
        form = ChangePassForm()
        return render(request, 'pages/change-pass.html', {'form': form, 'errors': ''})
    
    login = Login(request)
    form = ChangePassForm(request.POST)
    if not form.is_valid():
        errors = json.dumps(form.errors)
        return render(request, 'pages/change-pass.html', {'form': form, 'errors': errors})
    
    with suppress(AuthenticationError):
        data = form.cleaned_data
        login.cahnge_pass_and_auth(data['login'], data['old_pass'], data['new_pass'])
        return redirect('start_page')

    return JsonResponse(
        {'errors': json.dumps(
            {'login': [{'message': 'Неверный логин или пароль'},]}
        )}
    )
