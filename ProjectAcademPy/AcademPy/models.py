from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    dt_nascimento = models.DateField()
    foto = models.ImageField(blank=True, null=True, upload_to='perfil/')
