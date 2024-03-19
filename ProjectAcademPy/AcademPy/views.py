from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Administrador, Professor, Turma, Disciplina, Aula, Cronograma

def cadastro_adm_view(request):
    """
    Permite o cadastro de novos administradores.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página de cadastro de administrador com formulário vazio no método GET.
        Redireciona para a página de conta do usuário após o cadastro bem-sucedido no método POST.
        Retorna uma resposta de erro BadRequest para outros métodos de requisição.

    """
    if request.method == 'GET':
        # Se a requisição for do tipo GET, renderiza o formulário de cadastro de administrador vazio.
        return render(request, 'cadastro_adm.html', {
            "email_repeated": False,
            "cod_invalid": False,
            "password_invalid": False,
        })
    elif request.method == 'POST':
        # Se a requisição for do tipo POST, processa os dados do formulário de cadastro.
        cod_academ = request.POST.get('cod_academ')
        # Verifica se o código acadêmico é válido.
        if cod_academ != '1234567890':
            return render(request, 'cadastro_adm.html', {
                "cod_invalid": True,
            })

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        # Verifica se o email já está em uso.
        if User.objects.filter(email=email).count() > 0:
            return render(request, 'cadastro_adm.html', {
                "email_repeated": True,
            })
        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')
        # Verifica se as senhas coincidem.
        if confirma_password != password:
            return render(request, 'cadastro_adm.html', {
                "password_invalid": True,
            })

        # Cria o usuário no sistema.
        user = User.objects.create_user(email, email, password)
        user.first_name = nome.split(' ')[0]
        user.last_name = nome.split(' ')[-1]
        user.save()
        
        # Cria o objeto Administrador associado ao usuário.
        administrador = Administrador()
        administrador.usuario = user
        administrador.cod_academ = cod_academ
        administrador.save()
        
        # Faz login do usuário recém-criado e redireciona para a página de conta.
        login(request, user)
        return HttpResponseRedirect('/minha-conta')
    else:
        # Retorna uma resposta de erro BadRequest para métodos de requisição desconhecidos.
        return HttpResponseBadRequest()


def cadastro_professor_view(request):
    """
    Permite o cadastro de novos professores.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página de cadastro de professor com formulário vazio no método GET.
        Redireciona para a página de conta do usuário após o cadastro bem-sucedido no método POST.
        Retorna uma resposta de erro BadRequest para outros métodos de requisição.

    """
    # Obtém todas as disciplinas para exibir no formulário de cadastro.
    disciplinas = Disciplina.objects.all()
    if request.method == 'GET':
        # Se a requisição for do tipo GET, renderiza o formulário de cadastro de professor com as disciplinas disponíveis.
        return render(request, 'cadastro_professor.html', {
            'disciplinas': disciplinas,
            "email_repeated": False,
            "cod_invalido": False,
        })
    elif request.method == 'POST':
        # Se a requisição for do tipo POST, processa os dados do formulário de cadastro.
        cod_academ = request.POST.get('cod_academ')
        # Verifica se o código acadêmico é válido.
        if cod_academ != '0987654321':
            return render(request, 'cadastro_professor.html', {
                "cod_invalido": True,
            })

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        # Verifica se o email já está em uso.
        if User.objects.filter(email=email).count() > 0:
            return render(request, 'cadastro_professor.html', {
                "email_repeated": True,
            })
        especializacao = request.POST.get('especializacao')
        
        # Verifica a disponibilidade do professor nos diferentes turnos.
        disponibilidade_manha = True if request.POST.get('manha') is not None else False
        disponibilidade_tarde = True if request.POST.get('tarde') is not None else False
        disponibilidade_noite = True if request.POST.get('noite') is not None else False

        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')
        # Verifica se as senhas coincidem.
        if confirma_password != password:
            return render(request, 'cadastro_adm.html', {
                "password_invalid": True,
            })
        
        # Cria o usuário no sistema.
        user = User.objects.create_user(email, email, password)
        user.first_name = nome.split(' ')[0]
        user.last_name = nome.split(' ')[-1]
        user.save()
        
        # Cria o objeto Professor associado ao usuário.
        professor = Professor()
        professor.usuario = user
        professor.especializacao = especializacao
        professor.disponibilidade_manha = disponibilidade_manha
        professor.disponibilidade_tarde = disponibilidade_tarde
        professor.disponibilidade_noite = disponibilidade_noite
        professor.cod_academ = cod_academ
        professor.save()
        
        # Faz login do usuário recém-criado e redireciona para a página de conta.
        login(request, user)
        return HttpResponseRedirect('/minha-conta')
    else:
        # Retorna uma resposta de erro BadRequest para métodos de requisição desconhecidos.
        return HttpResponseBadRequest()


@login_required(login_url='/entrar')
def criar_cronograma_view(request):
    """
    Permite a criação de cronogramas para turmas existentes.
    """
    turmas = Turma.objects.all()
    if request.method == 'GET':
        return render(request, 'criar_cronograma.html', {
            'turmas': turmas,
        })

    elif request.method == 'POST':
        turno = request.POST.get("turno")
        dias_semana = request.POST.getlist("dias_semana")
        qtd_aulas = request.POST.get("qtd_aulas")
        turmas = request.POST.getlist("turmas")
        return HttpResponse(str(dias_semana))

    else:
        return HttpResponseBadRequest()


@login_required(login_url='/entrar')
def cronograma_view(request):
    disciplinas = Disciplina.objects.all()
    professores = Professor.objects.all()

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
        'disciplinas': disciplinas,
        'professores': professores,
        'dias_semana': list(range(2,2+QTD_DIAS_SEMANA)),  # Dias da semana de segunda a sexta.
        'turmas': list(range(1,1+QTD_TURMAS)),  # Números de turmas de 1 a 3.
        'horarios': list(range(1,1+QTD_HORARIOS)),  # Números de horários de 1 a 4.
        'professor_sobreposto': False,
    })

@login_required(login_url='/entrar')
def disciplinas_view(request):
    """
    Permite visualizar as disciplinas existentes e adicionar novas.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página de disciplinas com as disciplinas existentes no método GET.
        Adiciona uma nova disciplina e renderiza a página de disciplinas no método POST.
        Retorna uma resposta de erro BadRequest para outros métodos de requisição.
    """
    # Obtém todas as disciplinas para exibir na página.
    disciplinas = Disciplina.objects.all()
    if request.method == 'GET':
        # Se a requisição for do tipo GET, renderiza a página de disciplinas com as disciplinas existentes.
        return render(request, 'disciplinas.html', {
            'disciplinas': disciplinas,
            "disciplina_repetida": False,
        })
    elif request.method == 'POST':
        # Se a requisição for do tipo POST, processa os dados do formulário de adição de disciplina.
        entrada_nome_disciplina = request.POST.get("nome_disciplina")
        nome_disciplina = entrada_nome_disciplina.upper()

        # Verifica se a disciplina já existe no banco de dados.
        if Disciplina.objects.filter(nome=nome_disciplina).exists():
            # Se a disciplina já existe, renderiza a página de disciplinas novamente com uma mensagem de erro.
            return render(request, 'disciplinas.html', {
            'disciplinas': disciplinas,
            'disciplina_repetida': True,
        })
        else:
            # Se a disciplina não existe, cria uma nova e a salva no banco de dados.
            disciplina = Disciplina()
            disciplina.nome = nome_disciplina
            disciplina.save()
            # Renderiza a página de disciplinas novamente após adicionar a nova disciplina.
            return render(request, 'disciplinas.html', {
                'disciplinas': disciplinas,
            })
    else:
        # Retorna uma resposta de erro BadRequest para métodos de requisição desconhecidos.
        return HttpResponseBadRequest()


@login_required(login_url='/entrar')
def editar_disciplina_view(request, id):
    """
    Permite editar o nome de uma disciplina existente.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.
        id (int): O ID da disciplina a ser editada.

    Returns:
        HttpResponse: Renderiza a página de edição de disciplina com o formulário preenchido com os dados da disciplina no método GET.
        Atualiza o nome da disciplina no banco de dados e renderiza a página de edição de disciplina no método POST.
    """
    # Obtém a disciplina a ser editada pelo seu ID.
    disciplina = Disciplina.objects.get(id=id)
    # Obtém todas as disciplinas para exibir no formulário de edição.
    disciplinas = Disciplina.objects.all()
    if request.method == 'GET':
        # Se a requisição for do tipo GET, renderiza a página de edição de disciplina com o formulário preenchido.
        return render(request, 'editar_disciplina.html', {
            'disciplina': disciplina,
            'disciplina_repetida': False,
        })
    elif request.method == 'POST':
        # Se a requisição for do tipo POST, processa os dados do formulário de edição.
        entrada_nome_disciplina = request.POST.get("nome_disciplina")
        nome_disciplina = entrada_nome_disciplina.upper()

        # Verifica se o novo nome da disciplina já existe no banco de dados.
        if Disciplina.objects.filter(nome=nome_disciplina).exists():
            # Se o novo nome já existe, renderiza a página de edição novamente com uma mensagem de erro.
            return render(request, 'editar_disciplina.html', {
                'disciplina': disciplina,
                'disciplinas': disciplinas,
                'disciplina_repetida': True,
            })
        else:
            # Se o novo nome não existe, atualiza o nome da disciplina e salva no banco de dados.
            disciplina.nome = nome_disciplina
            disciplina.save()
            # Renderiza a página de edição novamente após a atualização.
            return render(request, 'editar_disciplina.html', {
                'disciplina': disciplina,
            })
    else:
        return HttpResponseBadRequest()


@login_required(login_url='/entrar')
def editar_turma_view(request, id):
    """
    Permite editar o nome ou o turno de uma turma existente.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.
        id (int): O ID da turma a ser editada.

    Returns:
        HttpResponse: Renderiza a página de edição de turma com o formulário preenchido com os dados da turma no método GET.
        Atualiza o nome ou o turno da turma no banco de dados e renderiza a página de edição de turma no método POST.
    """
    # Obtém a turma a ser editada pelo seu ID.
    turma = Turma.objects.get(id=id)
    # Obtém todas as turmas para exibir no formulário de edição.
    turmas = Turma.objects.all()
    turmas = Turma.objects.all()
    if request.method == 'GET':
        # Se a requisição for do tipo GET, renderiza a página de edição de turma com o formulário preenchido.
        return render(request, 'editar_turma.html', {
            'turma': turma,
            "turma_repetida": False,
        })
    elif request.method == 'POST':
        # Se a requisição for do tipo POST, processa os dados do formulário de edição.
        if 'edita_nome_turma' in request.POST:
            # Se o formulário é para editar o nome da turma.
            entrada_nome_turma = request.POST.get("nome_turma")
            nome_turma = entrada_nome_turma.upper()

            turno_turma = turma.turno

            # Verifica se o novo nome da turma já existe para o mesmo turno.
            if Turma.objects.filter(turno=turno_turma).filter(nome=nome_turma).exists():
                # Se o novo nome já existe, renderiza a página de edição novamente com uma mensagem de erro.
                return render(request, 'editar_turma.html', {
                    'turma': turma,
                    'turmas': turmas,
                    'turma_repetida': True,
                })
            else:
                # Se o novo nome não existe, atualiza o nome da turma e salva no banco de dados.
                turma.nome = nome_turma
                turma.save()
                # Renderiza a página de edição novamente após a atualização.
                return render(request, 'editar_turma.html', {
                    'turma': turma,
                })

        elif 'edita_turno_turma' in request.POST:
            # Se o formulário é para editar o turno da turma.
            turno_turma = request.POST.get("turno_turma")

            nome_turma = turma.nome

            # Verifica se já existe outra turma com o mesmo nome e turno.
            if Turma.objects.filter(turno=turno_turma).filter(nome=nome_turma).exists():
                # Se já existe outra turma com o mesmo nome e turno, renderiza a página de edição novamente com uma mensagem de erro.
                return render(request, 'editar_turma.html', {
                'turma': turma,
                'turmas': turmas,
                'turma_repetida': True,
            })
            else:
                # Se não existe outra turma com o mesmo nome e turno, atualiza o turno da turma e salva no banco de dados.
                turma.turno = turno_turma
                turma.save()
                # Renderiza a página de edição novamente após a atualização.
                return render(request, 'editar_turma.html', {
                'turma': turma,
            })
    else:
        return HttpResponseBadRequest()


def entrar_view(request):
    """
    Permite que os usuários façam login em suas contas.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página de login com um formulário vazio no método GET.
        Verifica as credenciais de login no método POST e redireciona para a página inicial se as credenciais forem válidas.
        Retorna uma mensagem de erro na página de login se as credenciais forem inválidas.
    """
    if request.method == 'GET':
        # Se a requisição for do tipo GET, renderiza a página de login com um formulário vazio.
        return render(request, 'entrar.html', {
            'incorrect_login': False
        })
    elif request.method == 'POST':
        # Se a requisição for do tipo POST, verifica as credenciais de login.
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        # Verifica se as credenciais são válidas.
        if user is not None:
            # Se as credenciais forem válidas, faz o login do usuário e redireciona para a página inicial.
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            # Se as credenciais forem inválidas, renderiza a página de login com uma mensagem de erro.
            return render(request, 'entrar.html', {
                'incorrect_login': True
            })
    else:
        # Se a requisição for de um tipo diferente de GET ou POST, retorna um erro HTTP 400 (Bad Request).
        return HttpResponseBadRequest()


@login_required(login_url='/entrar')
def excluir_disciplina_view(request, id):
    """
    Permite excluir disciplinas existentes.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.
        id (int): O ID da disciplina a ser excluída.

    Returns:
        HttpResponseRedirect: Redireciona para a página de disciplinas após a exclusão.

    Raises:
        Disciplina.DoesNotExist: Se a disciplina com o ID fornecido não existe.
    """
    # Obtém a disciplina com o ID fornecido.
    disciplina = Disciplina.objects.get(id=id)
    # Exclui a disciplina do banco de dados.
    disciplina.delete()
    # Redireciona para a página de disciplinas.
    return HttpResponseRedirect('/disciplinas')


@login_required(login_url='/entrar')
def excluir_turma_view(request, id):
    """
    Permite excluir turmas existentes.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.
        id (int): O ID da turma a ser excluída.

    Returns:
        HttpResponseRedirect: Redireciona para a página de turmas após a exclusão.

    Raises:
        Turma.DoesNotExist: Se a turma com o ID fornecido não existe.
    """
    # Obtém a turma com o ID fornecido.
    turma = Turma.objects.get(id=id)
    # Exclui a turma do banco de dados.
    turma.delete()
    # Redireciona para a página de turmas.
    return HttpResponseRedirect('/turmas')


# Definir constantes para o número de dias da semana, turmas e horários
QTD_DIAS_SEMANA = 1
QTD_TURMAS = 3
QTD_HORARIOS = 4

@login_required(login_url='/entrar')
def gerar_cronograma_view(request):
    def valida_cronograma():
        aulas_alocadas_por_professor = {}
        # --- Preenchimento do dicionário 'aulas_alocadas_por_professor' ---
        for dia_semana in range(2, 2 + QTD_DIAS_SEMANA):
            for turma in range(1, 1 + QTD_TURMAS):
                for horario in range(1, 1 + QTD_HORARIOS):
                    disciplina_key = f'disciplina_{dia_semana}_{turma}_{horario}'
                    professor_key = f'professor_{dia_semana}_{turma}_{horario}'
                    disciplina_id_str = request.POST.get(disciplina_key)
                    professor_id_str = request.POST.get(professor_key)

                    if not disciplina_id_str or not professor_id_str:  # Verifica se os campos do form estão vazios
                        continue

                    # Convertendo para int apenas se os campos não estão vazios
                    disciplina_id = int(disciplina_id_str)
                    professor_id = int(professor_id_str)

                    # As próximas linhas de código só são executadas caso a aula não seja vaga
                    aula_alocada = (dia_semana, horario)
                    if professor_id in aulas_alocadas_por_professor.keys(): # Verifica se o professor_id já existe no dicionário
                        for aula in aulas_alocadas_por_professor[professor_id]:
                            if aula[0] == dia_semana and aula[1] == horario:
                                return True  # Retorna True se houver um conflito
                        aulas_alocadas_por_professor[professor_id].append(aula_alocada)
                    else:
                        aulas_alocadas_por_professor[professor_id] = [aula_alocada]

        return False  # Retorna False se não houver conflitos

    disciplinas = Disciplina.objects.all()
    professores = Professor.objects.all()

    if request.method == 'GET':
        return render(request, 'gerar_cronograma.html', {
            'disciplinas': disciplinas,
            'professores': professores,
            'dias_semana': list(range(2, 2 + QTD_DIAS_SEMANA)),  # Dias da semana de segunda a sexta.
            'turmas': list(range(1, 1 + QTD_TURMAS)),  # Números de turmas de 1 a 3.
            'horarios': list(range(1, 1 + QTD_HORARIOS)),  # Números de horários de 1 a 4.
            'professor_sobreposto': False,
        })
    elif request.method == 'POST':
        # --- Validação ---
        if valida_cronograma():
            # Se houver conflitos, exibe na tela os conflitos encontrados
            return render(request, 'gerar_cronograma.html', {
                'disciplinas': disciplinas,
                'professores': professores,
                'dias_semana': list(range(2, 2 + QTD_DIAS_SEMANA)),  # Dias da semana de segunda a sexta.
                'turmas': list(range(1, 1 + QTD_TURMAS)),  # Números de turmas de 1 a 3.
                'horarios': list(range(1, 1 + QTD_HORARIOS)),  # Números de horários de 1 a 4.
                'professor_sobreposto': True,
            })

        # Se não houver conflitos, cadastra o cronograma e redireciona para a página de cronograma gerado
        cronograma = Cronograma.objects.create()  # Cria um objeto Cronograma vazio
        for dia_semana in range(2, 2 + QTD_DIAS_SEMANA):
            for turma in range(1, 1 + QTD_TURMAS):
                for horario in range(1, 1 + QTD_HORARIOS):
                    disciplina_key = f"disciplina_{dia_semana}_{turma}_{horario}"
                    professor_key = f"professor_{dia_semana}_{turma}_{horario}"
                    disciplina_id_str = request.POST.get(disciplina_key)
                    professor_id_str = request.POST.get(professor_key)

                    if not disciplina_id_str or not professor_id_str:
                        continue

                    disciplina_id = int(disciplina_id_str)
                    professor_id = int(professor_id_str)

                    disciplina = Disciplina.objects.get(id=disciplina_id)
                    professor = Professor.objects.get(id=professor_id)

                    # Cria a instância da aula no banco de dados
                    Aula.objects.create(
                        cronograma=cronograma,
                        turma=turma,
                        disciplina=disciplina,
                        professor=professor,
                        dia_semana=dia_semana,
                        horario=horario
                    )

        return redirect('/cronograma/')

    else:
        return HttpResponseBadRequest()


@login_required(login_url='/entrar')
def home_view(request):
    if Administrador.objects.filter(usuario=request.user).exists():
        total_professores = Professor.objects.all().count() - 1  # Desconta 1 porque um é '@VAGA'
        total_disciplinas = Disciplina.objects.all().count() - 1  # Desconta 1 porque uma é '@VAGA'
        total_turmas = Turma.objects.all().count()
        total_turmas_manha = Turma.objects.filter(turno='manha').count()
        total_turmas_tarde = Turma.objects.filter(turno='tarde').count()
        total_turmas_noite = Turma.objects.filter(turno='noite').count()
        return render(request, 'home_adm.html', {
            'username': request.user.username,
            'total_professores': total_professores,
            'total_disciplinas': total_disciplinas,
            'total_turmas': total_turmas,
            'total_turmas_manha': total_turmas_manha,
            'total_turmas_tarde': total_turmas_tarde,
            'total_turmas_noite': total_turmas_noite,
        })
    elif Professor.objects.filter(usuario=request.user).exists():
        return render(request, 'home_professor.html', {
            'username': request.user.username,
        })
    else:
        return HttpResponseRedirect('/entrar')


def index_view(request):
    """
    Renderiza a página inicial do site.
    """
    return render(request, 'index.html')


@login_required(login_url='/entrar')
def logout_view(request):
    """
    Permite que os usuários façam logout de suas contas.
    """
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/entrar')
def minha_conta_view(request):
    """
    Permite que os usuários visualizem e editem suas informações de conta.

    Esta função determina o tipo de conta do usuário (administrador ou professor) e renderiza
    a página correspondente 'minha_conta_adm.html' para administradores e 'minha_conta_professor.html'
    para professores. Se o usuário não for nem administrador nem professor, ele é redirecionado para
    a página de login.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página de visualização e edição de informações de conta correspondente.

    Raises:
        None
    """
    if Administrador.objects.filter(usuario=request.user).exists():
        # Se o usuário for um administrador, obtém e renderiza as informações da conta de administrador.
        if request.method == 'GET':
            return render(request, 'minha_conta_adm.html', {
                'username': request.user.username,
            })
        elif request.method == 'POST':
            administradores = Administrador.objects.all()
            if 'edita_nome' in request.POST:
                nome = request.POST.get("nome")

                email = administradores.usuario.email
                first_name = administradores.usuario.first_name
                last_name = administradores.usuario.last_name
                password = administradores.usuario.password

                administradores.first_name = nome.split(' ')[0]
                administradores.last_name = nome.split(' ')[-1]
                administradores.save()

                return render(request, 'minha_conta_adm.html', {
                    'username': request.user.username,
                })
        else:
            return HttpResponseBadRequest()
    elif Professor.objects.filter(usuario=request.user).exists():
    # Se o usuário for um professor, obtém as informações da conta de professor e as disciplinas associadas.
        if request.method == 'GET':
            professor = Professor.objects.get(usuario=request.user)
            disciplinas = Disciplina.objects.all()
            return render(request, 'minha_conta_professor.html', {
                'username': request.user.username,
                'nome': request.user.first_name + " " + request.user.last_name,
                'email': request.user.email,
                'professor': professor,
                'disciplinas': disciplinas,
            })
        elif request.method == 'POST':
            pass
    else:
        # Se o usuário não for nem administrador nem professor, redireciona para a página de login.
        return HttpResponseRedirect('/entrar')


@login_required(login_url='/entrar')
def professores_view(request):
    """
    Permite visualizar os professores cadastrados.

    Esta função recupera todos os professores cadastrados no sistema e os filtra com base em sua disponibilidade
    de horário de acordo com os períodos da manhã, tarde e noite. Em seguida, renderiza a página 'professores.html'
    com as informações dos professores para exibição.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página 'professores.html' com informações dos professores cadastrados.

    Raises:
        None
    """
    # Recupera todos os professores cadastrados no sistema
    professores = Professor.objects.all()

    # Filtra os professores com disponibilidade de horário pela manhã, tarde e noite
    professores_manha = Professor.objects.filter(disponibilidade_manha="1")
    professores_tarde = Professor.objects.filter(disponibilidade_tarde="1")
    professores_noite = Professor.objects.filter(disponibilidade_noite="1")

    # Renderiza a página 'professores.html' com as informações dos professores
    return render(request, 'professores.html', {
        'professores': professores,
        'professores_manha': professores_manha,
        'professores_tarde': professores_tarde,
        'professores_noite': professores_noite,
    })


def redes_sociais_view(request):
    """
    Renderiza a página de redes sociais do site.
    """
    return render(request, 'redes_sociais.html')


@login_required(login_url='/entrar')
def turmas_view(request):
    """
    Permite visualizar as turmas existentes e adicionar novas.

    Esta função recupera todas as turmas cadastradas no sistema e as filtra de acordo com seus turnos (manhã, tarde, noite).
    Em seguida, renderiza a página 'turmas.html' com as informações das turmas para exibição e permite a adição de novas
    turmas através de um formulário.

    Parameters:
        request (HttpRequest): O objeto de requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página 'turmas.html' com informações das turmas cadastradas e o formulário para adição de novas turmas.

    Raises:
        None
    """
    # Recupera todas as turmas cadastradas no sistema
    turmas = Turma.objects.all()

    # Filtra as turmas de acordo com o turno (manhã, tarde, noite)
    manha = Turma.objects.filter(turno="manha")
    tarde = Turma.objects.filter(turno="tarde")
    noite = Turma.objects.filter(turno="noite")

    if request.method == 'GET':
        # Se a requisição for do tipo GET, renderiza a página 'turmas.html' com as informações das turmas e o formulário
        # para adição de novas turmas
        return render(request, 'turmas.html', {
            'turmas': turmas,
            'manha': manha,
            'tarde': tarde,
            'noite': noite,
            "turma_repetida": False,
        })
    elif request.method == 'POST':
        # Se a requisição for do tipo POST, adiciona uma nova turma
        entrada_nome_turma = request.POST.get("nome_turma")
        nome_turma = entrada_nome_turma.upper()
        turno_turma = request.POST.get("turno_turma")

        # Verifica se a turma já existe no sistema
        if Turma.objects.filter(turno=turno_turma).filter(nome=nome_turma).exists():
            return render(request, 'turmas.html', {
                'turmas': turmas,
                'manha': manha,
                'tarde': tarde,
                'noite': noite,
                'turma_repetida': True,
            })
        else:
            # Cria e salva a nova turma no banco de dados
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
        # Se a requisição não for nem GET nem POST, retorna um erro BadRequest
        return HttpResponseBadRequest()
