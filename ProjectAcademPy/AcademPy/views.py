from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from .models import Perfil

def cadastro_view(request):
    return render(request, 'cadastro.html', {
        'username': request.user.username
    })

def home_view(request):
    return render(request, 'home.html', {
        'username': request.user.username
    })

def horarios_materias_view(request):
    return render(request, 'horarios_materias.html', {
        'username': request.user.username
    })

def login_view(request):
    return render(request, 'login.html', {
        'username': request.user.username
    })
