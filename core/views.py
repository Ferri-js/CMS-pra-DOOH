from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404 
from .models import Midia, Playlist, ItemPlaylist, TipoDispositivo
from .forms import MidiaForm 
import time # Para simular o upload

# --- FUNÇÃO DE UPLOAD PARA O CLOUD (SIMULAÇÃO) ---
# SUBSTITUA ESTA FUNÇÃO PELA IMPLEMENTAÇÃO REAL DO SEU TIME!
def cadastrarmidiaPcloud(arquivo_django, tipo_midia):
    """Função que simula o envio para a Nuvem e retorna o URL público."""
    print(f"--- INICIANDO UPLOAD PARA CLOUD: {arquivo_django.name} ---")
    time.sleep(0.5) 
    
    # URL FICTÍCIO GERADO PELA NUVEM
    url_gerada = f"https://seuservidorcloud.com/midias/{arquivo_django.name.replace(' ', '_')}"
    
    print(f"--- UPLOAD CONCLUÍDO. URL GERADO: {url_gerada} ---")
    return url_gerada
# -------------------------------------------------------------


# --- FUNÇÃO 1: Player em Loop (URL '/') ---
def home(request):
    # ... (código existente da view home) ...
    playlist = Playlist.objects.filter(ativa=True).prefetch_related('itens__midia').first()
    context = {'playlist': playlist}
    return render(request, 'core/player_loop.html', context)


# --- FUNÇÃO 2: Painel de Gerenciamento Visual (URL /gerenciar/) ---
def gerenciar_midia(request):
    
    if request.method == 'POST':
        # Passa request.FILES
        form = MidiaForm(request.POST, request.FILES) 
        
        if form.is_valid():
            midia_instance = form.save(commit=False) 
            uploaded_file = midia_instance.arquivo_upload
            
            if uploaded_file:
                # 1. CHAMA A LÓGICA DO CLOUD E OBTÉM O URL PÚBLICO
                url_gerada = cadastrarmidiaPcloud(uploaded_file, midia_instance.tipo) 
                
                # 2. SALVA O URL GERADO NO CAMPO 'url_publica' DO MODEL
                midia_instance.url_publica = url_gerada
            
            midia_instance.save() 
            
            # Lógica HTMX para atualização
            if request.headers.get('Hx-Request'):
                 midias = Midia.objects.all().order_by('-data_upload')
                 return render(request, 'core/partials/midia_list.html', {'midias': midias})
            
            return redirect(reverse('gerenciar_midia'))
            
    else:
        form = MidiaForm() 

    midias = Midia.objects.all().order_by('-data_upload')

    context = {
        'midias': midias,
        'form': form,
    }
    return render(request, 'core/painel_midia.html', context)