from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from .models import Perfil
from django.contrib.auth.decorators import login_required

def cadastro_view(request):
    return render(request, 'cadastro.html', {
        'username': request.user.username
    })

def home_view(request):
    return render(request, 'home.html', {
        'username': request.user.username
    })

def login_view(request):
    return render(request, 'login.html', {
        'username': request.user.username
    })
    
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'incorrect_login': False
        })
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/minha-conta')
        else:
            return render(request, 'login.html', {
                'incorrect_login': True
            })
    else:
        return HttpResponseBadRequest()

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required(login_url='/login')
def minha_conta_view(request):
    return HttpResponseRedirect('/minha-conta', {
        'username': request.user.username,
    })

def minha_conta(request):
    perfil = Perfil.objects.get(usuario=request.user)
    return render(request, 'minha_conta.html', {
        'authenticated': True,
        'perfil': perfil,
        'username': request.user.username,
    })
