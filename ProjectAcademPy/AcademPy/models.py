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

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=5)

    class Meta:
        ordering = ['nome']

class Aula(models.Model):
    cronograma = models.ForeignKey(Cronograma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_semana = models.IntegerField()
    turma = models.IntegerField()
    horario = models.IntegerField()
