from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ['nome']

class Professor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    especializacao = models.CharField(max_length=100)
    disponibilidade_manha = models.BooleanField()
    disponibilidade_tarde = models.BooleanField()
    disponibilidade_noite = models.BooleanField()

class Cronograma(models.Model):
    dt_criacao = models.DateTimeField(auto_now_add=True)
    qtd_aulas = models.IntegerField()

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=5)
    qtd_aulas = models.IntegerField(default=6)

    class Meta:
        ordering = ['nome']

class Aula(models.Model):
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[(1, 'Domingo'), (2, 'Segunda-Feira'), (3, 'Terça-Feira'), (4, 'Quarta-Feira'), (5, 'Quinta-Feira'), (6, 'Sexta-Feira'), (7, 'Sábado')])
    horario = models.IntegerField()
