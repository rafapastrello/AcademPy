"""
URL configuration for ProjectAcademPy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AcademPy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view),
    path('cadastro/', views.cadastro_view),
    path('entrar/', views.entrar_view),
    path('home/', views.home_view),
    path('login/', views.login_view),
    path('login-e-seguranca/', views.login_e_seguranca_view),
    path('logout/', views.logout_view),
    path('minha-conta/', views.minha_conta_view),
    path('sobre/', views.sobre_view),
    path('redes-sociais/', views.redes_sociais_view),
]
