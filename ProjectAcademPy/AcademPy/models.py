from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    """
    Representa um administrador do sistema.

    Atributos:
        usuario (User): O usuário associado ao administrador.
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Disciplina(models.Model):
    """
    Representa uma disciplina.

    Atributos:
        nome (str): O nome da disciplina.
    """
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ['nome']

class Professor(models.Model):
    """
    Representa um professor.

    Atributos:
        usuario (User): O usuário associado ao professor.
        especializacao (str): A especialização do professor.
        disponibilidade_manha (bool): Disponibilidade do professor pela manhã.
        disponibilidade_tarde (bool): Disponibilidade do professor pela tarde.
        disponibilidade_noite (bool): Disponibilidade do professor pela noite.
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    especializacao = models.CharField(max_length=100)
    disponibilidade_manha = models.BooleanField()
    disponibilidade_tarde = models.BooleanField()
    disponibilidade_noite = models.BooleanField()

class Cronograma(models.Model):
    """
    Representa um cronograma de aulas.

    Atributos:
        dt_criacao (datetime): Data e hora de criação do cronograma.
        qtd_aulas (int): Quantidade total de aulas no cronograma.
        turno (str): Turno das aulas no cronograma.
    """
    dt_criacao = models.DateTimeField(auto_now_add=True)
    qtd_aulas = models.IntegerField()
    turno = models.CharField(max_length=5)

class Turma(models.Model):
    """
    Representa uma turma.

    Atributos:
        nome (str): O nome da turma.
        turno (str): O turno da turma.
        qtd_aulas (int): Quantidade total de aulas na turma (padrão 6).
    """
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=5)
    qtd_aulas = models.IntegerField(default=6)

    class Meta:
        ordering = ['nome']

class Aula(models.Model):
    """
    Representa uma aula.

    Atributos:
        cronograma (Cronograma): O cronograma associado à aula.
        turma (Turma): A turma associada à aula.
        disciplina (Disciplina): A disciplina associada à aula.
        professor (Professor): O professor associado à aula.
        dia_semana (int): O dia da semana da aula.
        horario (int): O horário da aula.
    """
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[(1, 'Domingo'), (2, 'Segunda-Feira'), (3, 'Terça-Feira'), (4, 'Quarta-Feira'), (5, 'Quinta-Feira'), (6, 'Sexta-Feira'), (7, 'Sábado')])
    horario = models.IntegerField()
