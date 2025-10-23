from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404 
from core.models import Midia, Playlist, Midia_Playlist, TipoDispositivo
from core.forms import MidiaForm 
import time # Para simular o upload

# --- FUNÇÃO 1: Player em Loop (URL '/') ---
def home(request):
    # ... (código existente da view home) ...
    playlist = Playlist.objects.filter(ativa=True).prefetch_related('itens__midia').first()
    context = {'playlist': playlist}
    return render(request, 'core/player_loop.html', context)