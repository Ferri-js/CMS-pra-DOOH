# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse

# Importa seus Models e Forms
from .models import (
    Midia, Playlist, ItemPlaylist, Dispositivo, TipoDispositivo
)
# 🚨 IMPORTANTE: Importa a função do Cloud
from .models import cadastrarmidiaPcloud 

from .forms import (
    MidiaForm, LoginForm, PlaylistForm, 
    ItemPlaylistForm, DispositivoForm
)
import time

# -------------------------------------------------------------
# FUNÇÕES PÚBLICAS (Sem login)
# -------------------------------------------------------------

def home(request):
    """View que serve como dashboard e lista os links principais."""
    return render(request, 'core/home.html', {})


def tela_verificacao(request):
    """View que verifica o código do dispositivo antes de liberar o player."""
    if request.method == 'POST':
        codigo = request.POST.get('codigo_verificacao')
        dispositivo = Dispositivo.objects.filter(codVerificacao=codigo).first()
        
        if dispositivo:
            request.session['dispositivo_id'] = dispositivo.pk
            messages.success(request, f"Dispositivo {dispositivo.nomeDispositivo} autorizado!")
            return redirect('player_exibicao') 
        else:
            messages.error(request, "Código de verificação inválido ou dispositivo não encontrado.")
            
    return render(request, 'core/verificacao.html', {})


def player_exibicao(request):
    """Busca a playlist associada ao dispositivo verificado e a envia para o player."""
    dispositivo_id = request.session.get('dispositivo_id')
    if not dispositivo_id:
        return redirect('verificacao') 

    try:
        dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
        playlist_obj = dispositivo.playlistAssociada 
        
        if playlist_obj and playlist_obj.ativa:
            # Pré-carrega os itens e mídias para o template iterar
            playlist_obj = Playlist.objects.prefetch_related('itens__midia').get(pk=playlist_obj.pk)
        else:
            playlist_obj = None
            
    except Dispositivo.DoesNotExist:
        if 'dispositivo_id' in request.session:
             del request.session['dispositivo_id'] 
        return redirect('verificacao')

    context = {'playlist': playlist_obj}
    # ⚠️ Usa o template 'player_loop.html' que você me enviou
    return render(request, 'core/player_loop.html', context)


# -------------------------------------------------------------
# AUTENTICAÇÃO (Login / Logout)
# -------------------------------------------------------------

def tela_login(request):
    if request.user.is_authenticated:
        return redirect('painel_gerenciamento')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or reverse('painel_gerenciamento')
            return redirect(next_url) 
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    else:
        form = LoginForm()
        
    context = {'form': form}
    return render(request, 'core/login.html', context)


@login_required
def tela_logout(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect('home')

# -------------------------------------------------------------
# PAINEL DE GERENCIAMENTO VISUAL (HTMX)
# -------------------------------------------------------------

# --- PÁGINA PRINCIPAL DO PAINEL (GET) ---
@login_required 
def painel_gerenciamento(request):
    """View principal que carrega o painel visual (substitui /gerenciar/)"""
    
    # Prepara todos os formulários e dados para o carregamento inicial
    context = {
        'form_midia': MidiaForm(),
        'form_playlist': PlaylistForm(),
        'form_dispositivo': DispositivoForm(),
        'midias': Midia.objects.all().order_by('-data_upload'),
        'playlists': Playlist.objects.all().order_by('titulo'),
        'dispositivos': Dispositivo.objects.all().order_by('nomeDispositivo'),
    }
    return render(request, 'core/painel_gerenciamento.html', context)


# --- VIEWS HTMX: MÍDIAS ---

@login_required
@require_POST
def upload_midia(request):
    """HTMX: Processa o upload de mídia."""
    form = MidiaForm(request.POST, request.FILES)
    
    if form.is_valid():
        midia_instance = form.save(commit=False)
        uploaded_file = midia_instance.arquivo_upload

        # Cenário 1: Tipo HTML (URL manual obrigatória)
        if midia_instance.tipo == 'HTML':
            if not midia_instance.url_publica:
                messages.error(request, "Tipo HTML exige um URL no campo 'URL de Exibição'.")
            else:
                 midia_instance.save()
                 messages.success(request, f'Mídia (HTML) "{midia_instance.titulo}" salva.')
        
        # Cenário 2: Vídeo ou Imagem (Upload de arquivo obrigatório)
        elif uploaded_file:
            try:
                # 🚨 Aqui chamamos a função do Cloud 🚨
                url_gerada = cadastrarmidiaPcloud(uploaded_file, midia_instance.tipo) 
                if url_gerada:
                    midia_instance.url_publica = url_gerada
                    midia_instance.save() 
                    messages.success(request, f'Mídia "{midia_instance.titulo}" salva e enviada para o Cloud.')
                else:
                    messages.error(request, 'Falha ao gerar URL do Cloud (função retornou None).')
            except Exception as e:
                messages.error(request, f'Erro interno no Cloud: {e}')
        
        # Cenário 3: Erro (Ex: Tipo Vídeo sem arquivo)
        else:
             messages.error(request, "Tipo Vídeo/Imagem exige o 'Arquivo de Upload'.")
    
    else:
        # Formulário inválido
        messages.error(request, f"Formulário de mídia inválido: {form.errors.as_text()}")

    # Resposta HTMX: retorna a lista de mídias atualizada
    midias = Midia.objects.all().order_by('-data_upload')
    response = render(request, 'core/partials/midia_list.html', {'midias': midias})
    response['HX-Trigger'] = 'midia-atualizada' # Avisa outros componentes para recarregar
    return response


@login_required
@require_GET
def lista_midias(request):
    """HTMX: Retorna apenas a lista de mídias."""
    midias = Midia.objects.all().order_by('-data_upload')
    return render(request, 'core/partials/midia_list.html', {'midias': midias})


# --- VIEWS HTMX: PLAYLISTS ---

@login_required
@require_POST
def criar_playlist(request):
    """HTMX: Processa a criação de uma nova playlist."""
    form = PlaylistForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Nova playlist criada!')
    else:
        messages.error(request, 'Erro ao criar playlist (título duplicado?).')
    
    # Resposta HTMX: retorna a lista de playlists atualizada e um formulário limpo
    playlists = Playlist.objects.all().order_by('titulo')
    form_playlist = PlaylistForm()
    response = render(request, 'core/partials/playlist_list.html', {'playlists': playlists, 'form_playlist': form_playlist})
    response['HX-Trigger'] = 'playlist-atualizada' # Avisa o painel de dispositivos
    return response


@login_required
@require_GET
def lista_playlists(request):
    """HTMX: Retorna a lista de playlists."""
    playlists = Playlist.objects.all().order_by('titulo')
    form_playlist = PlaylistForm()
    return render(request, 'core/partials/playlist_list.html', {'playlists': playlists, 'form_playlist': form_playlist})


@login_required
@require_GET
def detalhe_playlist(request, playlist_id):
    """HTMX: Exibe os itens de uma playlist específica."""
    playlist = get_object_or_404(Playlist.objects.prefetch_related('itens__midia'), pk=playlist_id)
    
    context = {
        'playlist': playlist,
        'itens_da_playlist': playlist.itens.all(), # Itens ordenados (definido no Model Meta)
        'form_item': ItemPlaylistForm(), # Formulário para adicionar nova mídia
    }
    return render(request, 'core/partials/detalhe_playlist.html', context)


@login_required
@require_POST
def adicionar_item_playlist(request, playlist_id):
    """HTMX: Adiciona uma mídia a uma playlist."""
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    form = ItemPlaylistForm(request.POST)

    if form.is_valid():
        novo_item = form.save(commit=False)
        novo_item.playlist = playlist
        novo_item.save()
        messages.success(request, f"Mídia '{novo_item.midia.titulo}' adicionada.")
    else:
        messages.error(request, "Erro ao adicionar mídia (verifique a ordem).")

    # Resposta HTMX: Retorna os detalhes da playlist atualizados
    context = {
        'playlist': playlist,
        'itens_da_playlist': playlist.itens.all(),
        'form_item': ItemPlaylistForm(), 
    }
    response = render(request, 'core/partials/detalhe_playlist.html', context)
    response['HX-Trigger'] = 'item-adicionado' # Avisa o container de mensagens
    return response


@login_required
@require_GET # Usando GET para links <a> simples
def remover_item_playlist(request, item_id):
    """HTMX: Remove um item da playlist."""
    item = get_object_or_404(ItemPlaylist, pk=item_id)
    playlist = item.playlist # Salva a playlist ANTES de deletar
    item.delete()
    messages.info(request, "Item removido da playlist.")

    # Resposta HTMX: Retorna APENAS a lista de itens atualizada
    itens_da_playlist = playlist.itens.all()
    response = render(request, 'core/partials/playlist_itens_list.html', {'itens_da_playlist': itens_da_playlist})
    response['HX-Trigger'] = 'item-removido' # Avisa o container de mensagens
    return response

# --- VIEWS HTMX: DISPOSITIVOS (Implementação) ---

@login_required
@require_POST
def criar_dispositivo(request):
    """HTMX: Processa a criação de um novo dispositivo."""
    form = DispositivoForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Novo dispositivo criado!')
    else:
        # Pega o primeiro erro de validação (ex: código duplicado)
        erro_msg = next(iter(form.errors.values()))[0] 
        messages.error(request, f'Erro ao criar dispositivo: {erro_msg}')

    # Resposta HTMX: retorna a lista de dispositivos e um formulário limpo
    dispositivos = Dispositivo.objects.all().order_by('nomeDispositivo')
    form_dispositivo = DispositivoForm()
    response = render(request, 'core/partials/dispositivo_list_completo.html', {'dispositivos': dispositivos, 'form_dispositivo': form_dispositivo})
    response['HX-Trigger'] = 'dispositivo-atualizado' # Avisa o container de mensagens
    return response

@login_required
@require_GET
def lista_dispositivos(request):
    """HTMX: Retorna o bloco de formulário e lista de dispositivos."""
    dispositivos = Dispositivo.objects.all().order_by('nomeDispositivo')
    form_dispositivo = DispositivoForm()
    return render(request, 'core/partials/dispositivo_list_completo.html', {'dispositivos': dispositivos, 'form_dispositivo': form_dispositivo})


@login_required
@require_GET
def detalhe_dispositivo(request, dispositivo_id):
    """HTMX: Exibe o formulário de edição de um dispositivo."""
    dispositivo = get_object_or_404(Dispositivo, pk=dispositivo_id)
    form = DispositivoForm(instance=dispositivo) 
    
    return render(request, 'core/partials/detalhe_dispositivo.html', {'form_dispositivo': form, 'dispositivo': dispositivo})

@login_required
@require_POST
def editar_dispositivo(request, dispositivo_id):
    """HTMX: Salva as alterações de um dispositivo."""
    dispositivo = get_object_or_404(Dispositivo, pk=dispositivo_id)
    form = DispositivoForm(request.POST, instance=dispositivo)

    if form.is_valid():
        form.save()
        messages.success(request, f'Dispositivo "{dispositivo.nomeDispositivo}" atualizado.')
    else:
        messages.error(request, 'Erro ao salvar alterações.')

    # Resposta HTMX: Retorna o bloco de dispositivos (com formulário de criação)
    dispositivos = Dispositivo.objects.all().order_by('nomeDispositivo')
    form_dispositivo = DispositivoForm() 
    response = render(request, 'core/partials/dispositivo_list_completo.html', {'dispositivos': dispositivos, 'form_dispositivo': form_dispositivo})
    response['HX-Trigger'] = 'dispositivo-atualizado'
    return response