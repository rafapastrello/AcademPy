from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Administrador, Professor 

def cadastro_adm_view(request):
    if request.method == 'GET':
        return render(request, 'cadastro_adm.html', {
            "email_repeated": False
        })
    elif request.method == 'POST':
        cod_academ = request.POST.get('cod_academ')
        if cod_academ != '1234567890':
            return render(request, 'cadastro_adm.html', {
                "cod_invalido": True
            })

        username = request.POST.get('username')
        email = request.POST.get('email')
        if User.objects.filter(email=email).count() > 0:
            return render(request, 'cadastro_adm.html', {
                "email_repeated": True
            })

        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)

        administrador = Administrador()
        administrador.usuario = user
        administrador.cod_academ = cod_academ
        administrador.save()
        login(request, user)
        return HttpResponseRedirect('/minha-conta')
    else:
        return HttpResponseBadRequest()

def cadastro_professor_view(request):
    if request.method == 'GET':
        return render(request, 'cadastro_professor.html', {
            "email_repeated": False
        })
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
        return HttpResponseRedirect('/minha-conta')
    else:
        return HttpResponseBadRequest()

def entrar_view(request):
    if request.method == 'GET':
        return render(request, 'entrar.html', {
            'incorrect_login': False
        })
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        print(user) 
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/minha-conta')
        else:
            return render(request, 'entrar.html', {
                'incorrect_login': True
            })
    else:
        return HttpResponseBadRequest()

@login_required(login_url='/entrar')
def home_view(request):
    return render(request, 'home.html', {
        'username': request.user.username,
    })

def index_view(request):
    return render(request, 'index.html')

@login_required(login_url='/entrar')
def login_e_seguranca_view(request):
    return render(request, 'login_e_seguranca.html', {
        'username': request.user.username,
        'email': request.user.email,
    })

@login_required(login_url='/entrar')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/entrar')
def minha_conta_view(request):
    return render(request, 'minha_conta.html', {
        'username': request.user.username,
    })

def redes_sociais_view(request):
    return render(request, 'redes_sociais.html')

def sobre_view(request):
    return render(request, 'sobre.html')
