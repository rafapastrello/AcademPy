from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Administrador, Professor 

def cadastro_adm_view(request):
    if request.method == 'GET':
        return render(request, 'cadastro_adm.html', {
            "email_repeated": False,
            "cod_invalid": False,
            "password_invalid": False,
        })
    elif request.method == 'POST':
        cod_academ = request.POST.get('cod_academ')
        if cod_academ != '1234567890':
            return render(request, 'cadastro_adm.html', {
                "cod_invalid": True,
            })

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        if User.objects.filter(email=email).count() > 0:
            return render(request, 'cadastro_adm.html', {
                "email_repeated": True,
            })
        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')
        if confirma_password != password:
            return render(request, 'cadastro_adm.html', {
                "password_invalid": True,
            })
        
        user = User.objects.create_user(email, email, password)
        user.first_name = nome.split(' ')[0]
        user.last_name = nome.split(' ')[-1]
        user.save()
        
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
            "email_repeated": False,
            "cod_invalido": False,
        })
    elif request.method == 'POST':
        cod_academ = request.POST.get('cod_academ')
        if cod_academ != '0987654321':
            return render(request, 'cadastro_professor.html', {
                "cod_invalido": True,
            })

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        if User.objects.filter(email=email).count() > 0:
            return render(request, 'cadastro_professor.html', {
                "email_repeated": True,
            })
        especializacao = request.POST.get('especializacao')
        
        disponibilidade_manha = True if request.POST.get('manha') is not None else False
        disponibilidade_tarde = True if request.POST.get('tarde') is not None else False
        disponibilidade_noite = True if request.POST.get('noite') is not None else False

        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')
        if confirma_password != password:
            return render(request, 'cadastro_adm.html', {
                "password_invalid": True,
            })
        
        user = User.objects.create_user(email, email, password)
        user.first_name = nome.split(' ')[0]
        user.last_name = nome.split(' ')[-1]
        user.save()
        
        professor = Professor()
        professor.usuario = user
        professor.especializacao = especializacao
        #professor.disponibilidade = disponobilidade
        professor.disponibilidade_manha = disponibilidade_manha
        professor.disponibilidade_tarde = disponibilidade_tarde
        professor.disponibilidade_noite = disponibilidade_noite
        professor.cod_academ = cod_academ
        professor.save()
        
        login(request, user)
        return HttpResponseRedirect('/minha-conta')
    else:
        return HttpResponseBadRequest()
    
def criar_cronograma_view(request):
    return render(request, 'criar-cronograma.html')

def disciplinas_view(request):
    return render(request, 'disciplinas.html')

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
    if Administrador.objects.filter(usuario=request.user).exists():
        # É administrador
        return render(request, 'home_adm.html', {
            'username': request.user.username,
        })
    elif Professor.objects.filter(usuario=request.user).exists():
        # É professor
        return render(request, 'home_professor.html', {
            'username': request.user.username,
        })
    else:
        # Não é professor nem administrador
        return HttpResponseRedirect('/entrar')

def index_view(request):
    return render(request, 'index.html')

@login_required(login_url='/entrar')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/entrar')
def minha_conta_view(request):
    if Administrador.objects.filter(usuario=request.user).exists():
        # É administrador
        return render(request, 'minha_conta_adm.html', {
            'username': request.user.username,
            'nome': request.user.first_name + " " + request.user.last_name,
            'email': request.user.email,
        })
    elif Professor.objects.filter(usuario=request.user).exists():
        # É professor
        professor = Professor.objects.get(usuario=request.user)
        return render(request, 'minha_conta_professor.html', {
            'username': request.user.username,
            'nome': request.user.first_name + " " + request.user.last_name,
            'email': request.user.email,
            'professor': professor,
        })
    else:
        # Não é professor nem administrador
        return HttpResponseRedirect('/entrar')

def professores_view(request):
    return render(request, 'professores.html')

def redes_sociais_view(request):
    return render(request, 'redes_sociais.html')

def turmas_view(request):
    return render(request, 'turmas.html')
