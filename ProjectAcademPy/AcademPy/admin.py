from django.contrib import admin
from .models import Administrador, Disciplina, Professor, Turma

# Register your models here.

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    pass

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    pass

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    pass

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    pass
