from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Administrador, Professor, Turma, Disciplina, Aula, Cronograma

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
    disciplinas = Disciplina.objects.all()
    if request.method == 'GET':
        return render(request, 'cadastro_professor.html', {
            'disciplinas': disciplinas,
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

@login_required(login_url='/entrar')
def criar_cronograma_view(request):
    disciplinas = Disciplina.objects.all()
    professores = Professor.objects.all()
    professores_manha = Professor.objects.filter(disponibilidade_manha = "1")
    professores_tarde = Professor.objects.filter(disponibilidade_tarde = "1")
    professores_noite = Professor.objects.filter(disponibilidade_noite = "1")
    turmas = Turma.objects.all()
    if request.method == 'GET':
        return render(request, 'criar_cronograma.html', {
            'disciplinas': disciplinas,
            'professores': professores,
            'professores_manha': professores_manha,
            'professores_tarde': professores_tarde,
            'professores_noite': professores_noite,
            'turmas': turmas,
        })
    if request.method == 'POST':
        turno = request.POST.get("turno")
        dias_semana = request.POST.get("dias_semana")
        qtd_aulas = request.POST.get("qtd_aulas")
        disciplinas = request.POST.get("disciplinas")
        professores = request.POST.get("professores")
        turmas = request.POST.get("turmas")
        

@login_required(login_url='/entrar')
def cronograma_view(request):
    def obter_aulas(cronograma, turma, dia_semana):
        return Aula.objects.filter(cronograma=cronograma).filter(turma=turma).filter(dia_semana=dia_semana).order_by('horario')

    cronograma = Cronograma.objects.order_by('-dt_criacao').first()

    dias_da_semana = [
        (
            dia_semana, 
            [(turma.nome, obter_aulas(cronograma, turma, dia_semana)) for turma in Turma.objects.all()]
        ) 
        for dia_semana in range(1,8)
    ]

    return render(request, 'cronograma.html', {
        'dias_da_semana': dias_da_semana,
        'qtd_aulas': cronograma.qtd_aulas,
        'horarios_aulas': list(range(1, cronograma.qtd_aulas+1)) 
    })

@login_required(login_url='/entrar')
def disciplinas_view(request):
    disciplinas = Disciplina.objects.all()
    if request.method == 'GET':
        return render(request, 'disciplinas.html', {
            'disciplinas': disciplinas,
            "disciplina_repetida": False,
        })
    elif request.method == 'POST':
        entrada_nome_disciplina = request.POST.get("nome_disciplina")
        nome_disciplina = entrada_nome_disciplina.upper()

        if Disciplina.objects.filter(nome=nome_disciplina).exists():
            return render(request, 'disciplinas.html', {
            'disciplinas': disciplinas,
            'disciplina_repetida': True,
        })
        else:
            disciplina = Disciplina()
            disciplina.nome = nome_disciplina
            disciplina.save()
            return render(request, 'disciplinas.html', {
                'disciplinas': disciplinas,
            })
    else:
        return HttpResponseBadRequest()

@login_required(login_url='/entrar')
def editar_cronograma_view(request):
    if request.method == 'GET':
        return render(request, 'editar_cronograma.html')
    elif request.method == 'POST':
        pass

@login_required(login_url='/entrar')
def editar_disciplina_view(request, id):
    disciplina = Disciplina.objects.get(id=id)
    disciplinas = Disciplina.objects.all()
    if request.method == 'GET':
        return render(request, 'editar_disciplina.html', {
            'disciplina': disciplina,
            'disciplina_repetida': False,
        })
    elif request.method == 'POST':
        entrada_nome_disciplina = request.POST.get("nome_disciplina")
        nome_disciplina = entrada_nome_disciplina.upper()

        if Disciplina.objects.filter(nome=nome_disciplina).exists():
            return render(request, 'editar_disciplina.html', {
                'disciplina': disciplina,
                'disciplinas': disciplinas,
                'disciplina_repetida': True,
            })
        else:
            disciplina.nome = nome_disciplina
            disciplina.save()
            return render(request, 'editar_disciplina.html', {
                'disciplina': disciplina,
            })

@login_required(login_url='/entrar')
def editar_turma_view(request, id):
    turma = Turma.objects.get(id=id)
    turmas = Turma.objects.all()
    if request.method == 'GET':
        return render(request, 'editar_turma.html', {
            'turma': turma,
            "turma_repetida": False,
        })
    elif request.method == 'POST':
        if 'edita_nome_turma' in request.POST:
            entrada_nome_turma = request.POST.get("nome_turma")
            nome_turma = entrada_nome_turma.upper()

            turno_turma = turma.turno

            if Turma.objects.filter(turno=turno_turma).filter(nome=nome_turma).exists():
                return render(request, 'editar_turma.html', {
                    'turma': turma,
                    'turmas': turmas,
                    'turma_repetida': True,
                })
            else:
                turma.nome = nome_turma
                turma.save()
                return render(request, 'editar_turma.html', {
                    'turma': turma,
                })

        elif 'edita_turno_turma' in request.POST:
            turno_turma = request.POST.get("turno_turma")

            nome_turma = turma.nome

            if Turma.objects.filter(turno=turno_turma).filter(nome=nome_turma).exists():
                return render(request, 'editar_turma.html', {
                'turma': turma,
                'turmas': turmas,
                'turma_repetida': True,
            })
            else:
                turma.turno = turno_turma
                turma.save()
                return render(request, 'editar_turma.html', {
                'turma': turma,
            })

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
            return HttpResponseRedirect('/home')
        else:
            return render(request, 'entrar.html', {
                'incorrect_login': True
            })
    else:
        return HttpResponseBadRequest()

@login_required(login_url='/entrar')
def excluir_disciplina_view(request, id):
    disciplina = Disciplina.objects.get(id=id)
    disciplina.delete()
    return HttpResponseRedirect('/disciplinas')

@login_required(login_url='/entrar')
def excluir_turma_view(request, id):
    turma = Turma.objects.get(id=id)
    turma.delete()
    return HttpResponseRedirect('/turmas')

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
        disciplinas = Disciplina.objects.all()
        return render(request, 'minha_conta_professor.html', {
            'username': request.user.username,
            'nome': request.user.first_name + " " + request.user.last_name,
            'email': request.user.email,
            'professor': professor,
            'disciplinas': disciplinas,
        })
    else:
        # Não é professor nem administrador
        return HttpResponseRedirect('/entrar')

@login_required(login_url='/entrar')
def professores_view(request):
    professores = Professor.objects.all()
    professores_manha = Professor.objects.filter(disponibilidade_manha = "1")
    professores_tarde = Professor.objects.filter(disponibilidade_tarde = "1")
    professores_noite = Professor.objects.filter(disponibilidade_noite = "1")
    return render(request, 'professores.html', {
        'professores': professores,
        'professores_manha': professores_manha,
        'professores_tarde': professores_tarde,
        'professores_noite': professores_noite,
    })

def redes_sociais_view(request):
    return render(request, 'redes_sociais.html')

@login_required(login_url='/entrar')
def turmas_view(request):
    turmas = Turma.objects.all()
    manha = Turma.objects.filter(turno = "manha")
    tarde = Turma.objects.filter(turno = "tarde")
    noite = Turma.objects.filter(turno = "noite")
    if request.method == 'GET':    
        return render(request, 'turmas.html', {
            'turmas': turmas,
            'manha': manha,
            'tarde': tarde,
            'noite': noite,
            "turma_repetida": False,
        })
    elif request.method == 'POST':
        entrada_nome_turma = request.POST.get("nome_turma")
        nome_turma = entrada_nome_turma.upper()
        turno_turma = request.POST.get("turno_turma")

        if Turma.objects.filter(turno=turno_turma).filter(nome=nome_turma).exists():
            return render(request, 'turmas.html', {
                'turmas': turmas,
                'manha': manha,
                'tarde': tarde,
                'noite': noite,
                'turma_repetida': True,
            })
        else:
            turma = Turma()
            turma.nome = nome_turma
            turma.turno = turno_turma
            turma.save()
            return render(request, 'turmas.html', {
                'turmas': turmas,
                'manha': manha,
                'tarde': tarde,
                'noite': noite,
            })
    else:
        return HttpResponseBadRequest()
