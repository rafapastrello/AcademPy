from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cod_academ = models.CharField(max_length=10)

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)

class Professor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    disponibilidade = models.CharField(max_length=19)
    cod_academ = models.CharField(max_length=10)

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=5)