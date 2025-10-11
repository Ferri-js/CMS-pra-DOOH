from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404 # Útil para buscar objetos
from .models import Midia, Playlist, ItemPlaylist # Modelos Corretos
from .forms import MidiaForm # Formulário para o painel de gerenciamento

# --- FUNÇÃO 1: Player em Loop (Será carregada na URL raiz '/') ---
def home(request):
    """Busca a playlist ativa e a envia para o player de exibição (player_loop.html)."""
    
    # Busca a primeira playlist marcada como ATIVA e pre-carrega seus itens e mídias
    # O Model Playlist agora é o correto (sem o sufixo DB, após a limpeza)
    playlist = Playlist.objects.filter(ativa=True).prefetch_related('itens__midia').first()
    
    context = {
        'playlist': playlist
    }
    
    # O Player em Loop deve ser o template padrão da página principal
    return render(request, 'core/player_loop.html', context)

# --- FUNÇÃO 2: Painel de Gerenciamento Visual (URL /gerenciar/) ---
def gerenciar_midia(request):
    
    # Lógica para salvar dados do formulário (POST)
    if request.method == 'POST':
        form = MidiaForm(request.POST, request.FILES) # Adicionado request.FILES para uploads reais
        
        if form.is_valid():
            form.save()
            
            # Se a requisição for do HTMX, retorna APENAS a lista atualizada
            if request.headers.get('Hx-Request'):
                 midias = Midia.objects.all().order_by('-data_upload')
                 return render(request, 'core/partials/midia_list.html', {'midias': midias})
            
            # Se for um POST normal, redireciona
            return redirect(reverse('gerenciar_midia'))
            
    else:
        # Lógica para carregar a página (GET)
        form = MidiaForm() 

    # Busca todas as mídias para listar no painel
    midias = Midia.objects.all().order_by('-data_upload')

    context = {
        'midias': midias,
        'form': form,
    }
    
    # Renderiza o template do painel
    return render(request, 'core/painel_midia.html', context)