from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

class Professor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    especializacao = models.CharField(max_length=100)
    disponibilidade_manha = models.BooleanField()
    disponibilidade_tarde = models.BooleanField()
    disponibilidade_noite = models.BooleanField()

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=5)

class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=Professor)
    dia_semana = models.IntegerField(choices=[(1, 'Domingo'), (2, 'Segunda'), (3, 'Terça'), (4, 'Quarta'), (5, 'Quinta'), (6, 'Sexta'), (7, 'Sábado')])
    horario = models.IntegerField()
