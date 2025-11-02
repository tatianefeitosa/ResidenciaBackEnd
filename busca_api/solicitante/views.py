from django.shortcuts import render

# Create your views here.

def solicitante_home(request):
    return render(request, 'solicitante/solicitante-inicio.html')
