"""
URL configuration for ProjectAcademPy project.

The urlpatterns list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
    
Examples:
Function views:
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    
Class-based views:
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    
Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from AcademPy import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Rota para a página de administração do Django
    path('', views.index_view),  # Rota para a página inicial
    path('cadastro-adm/', views.cadastro_adm_view),  # Rota para o formulário de cadastro de administradores
    path('cadastro-professor/', views.cadastro_professor_view),  # Rota para o formulário de cadastro de professores
    path('criar-cronograma/', views.criar_cronograma_view),  # Rota para o formulário de criação de cronogramas
    path('disciplinas/', views.disciplinas_view),  # Rota para visualizar as disciplinas
    path('editar-disciplina/<int:id>', views.editar_disciplina_view, name='editar-disciplina'),  # Rota para editar uma disciplina específica
    path('editar-turma/<int:id>', views.editar_turma_view, name='editar-turma'),  # Rota para editar uma turma específica
    path('entrar/', views.entrar_view),  # Rota para a página de login
    path('excluir-disciplina/<int:id>', views.excluir_disciplina_view, name='excluir-disciplina'),  # Rota para excluir uma disciplina específica
    path('excluir-turma/<int:id>', views.excluir_turma_view, name='excluir-turma'),  # Rota para excluir uma turma específica
    path('home/', views.home_view),  # Rota para a página principal
    path('logout/', views.logout_view),  # Rota para fazer logout
    path('minha-conta/', views.minha_conta_view),  # Rota para visualizar e editar a conta do usuário
    path('professores/', views.professores_view),  # Rota para visualizar os professores
    path('redes-sociais/', views.redes_sociais_view),  # Rota para visualizar as redes sociais
    path('turmas/', views.turmas_view),  # Rota para visualizar as turmas
    path('cronograma/', views.cronograma_view, name='cronograma_view'),  # Rota para visualizar o cronograma
    path('gerar-cronograma/', views.gerar_cronograma_view, name='gerar_cronograma'),  # Rota para gerar cronogramas
]
