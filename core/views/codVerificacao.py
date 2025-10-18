from django.shortcuts import render, get_object_or_404
from core.models.dispositivo import Dispositivo

def dispositivo_view(request, codigo):
    disp = get_object_or_404(Dispositivo, codVerificacao=codigo)
    print(codigo)
    return render(request, 'core/codVerificacao.html', {'dispositivo':disp})

