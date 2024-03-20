from django.contrib import admin
from .models import Administrador, Disciplina, Professor, Turma, Cronograma, Aula

# Register your models here.

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    """
    Esta classe é usada para personalizar a exibição e o comportamento do modelo Administrador no painel de administração do Django.
    """

    pass

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    """
    Esta classe é usada para personalizar a exibição e o comportamento do modelo Disciplina no painel de administração do Django.
    """

    list_display = ['nome']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    """
    Esta classe é usada para personalizar a exibição e o comportamento do modelo Professor no painel de administração do Django.
    """
    pass

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    """
    Esta classe é usada para personalizar a exibição e o comportamento do modelo Turma no painel de administração do Django.
    """

    list_display = ['nome', 'turno']

@admin.register(Cronograma)
class CronogramaAdmin(admin.ModelAdmin):
    pass

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    pass