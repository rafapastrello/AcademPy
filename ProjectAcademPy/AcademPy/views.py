from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def horarios_materias_view(request):
    return render(request, 'horarios_materias.html')

