from django.shortcuts import render

# Create your views here.

def admin_inicio(request):
    return render(request, 'administracao/admin-inicio.html')

def admin_vagas(request):
    return render(request, 'administracao/vaga-solicitada.html')