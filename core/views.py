# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Importa seus Models e Forms
# 🚨 VERIFIQUE se a importação está correta após a consolidação em models.py
from .models import Midia, Playlist, ItemPlaylist, Dispositivo, TipoDispositivo
# 🚨 A função do Cloud está aqui ou em models.py? Ajuste o import se necessário.
from .models import cadastrarmidiaPcloud 

from .forms import MidiaForm, LoginForm
import time # Para a simulação do upload

# -------------------------------------------------------------
# LÓGICA DO CLOUD (SIMULAÇÃO) - O SEU TIME DEVE SUBSTITUIR ESTA FUNÇÃO
# (Mantida aqui por simplicidade, mas pode ser movida para utils.py)
def cadastrarmidiaPcloud(arquivo_django, tipo_midia):
    print(f"--- INICIANDO UPLOAD PARA CLOUD: {arquivo_django.name} ({tipo_midia}) ---")
    time.sleep(0.5)
    # Use um ID de arquivo e nome únicos para o URL de teste
    file_id_mock = hash(arquivo_django.name + str(time.time())) 
    safe_filename = arquivo_django.name.replace(' ', '_')
    url_gerada = f"https://u.pcloud.link/publink/show?code={file_id_mock}_{safe_filename}" 
    print(f"--- UPLOAD CONCLUÍDO. URL GERADO: {url_gerada} ---")
    return url_gerada
# -------------------------------------------------------------


# --- FUNÇÃO 1: Home Page / Dashboard (URL '/') ---
def home(request):
    """View que serve como dashboard e lista os links principais."""
    return render(request, 'core/home.html', {})


# --- FUNÇÃO 2: TELA DE VERIFICAÇÃO (URL /verificar/) ---
def tela_verificacao(request):
    """View que verifica o código do dispositivo antes de liberar o player."""

    if request.method == 'POST':
        codigo = request.POST.get('codigo_verificacao')

        try:
            dispositivo = Dispositivo.objects.get(codVerificacao=codigo)

            request.session['dispositivo_id'] = dispositivo.pk
            messages.success(request, f"Dispositivo {dispositivo.nomeDispositivo} autorizado!")
            return redirect('player_exibicao') # Redireciona para o Player

        except Dispositivo.DoesNotExist:
            messages.error(request, "Código de verificação inválido ou dispositivo não encontrado.")

    return render(request, 'core/verificacao.html', {})


# --- FUNÇÃO 3: Player de Exibição em Loop (URL /exibir/) ---
# VERSÃO REVERTIDA - Usa o objeto Playlist diretamente no template
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
        messages.error(request, "Dispositivo não encontrado. Verifique novamente.")
        return redirect('verificacao')

    # Envia o objeto Playlist completo (ou None) para o template
    context = {
        'playlist': playlist_obj 
    }
    
    return render(request, 'core/player_loop.html', context)


# --- FUNÇÃO 4: TELA DE LOGIN CUSTOMIZADA (URL /login/) ---
def tela_login(request):
    """View para exibir e processar o formulário de login customizado."""

    if request.user.is_authenticated:
        return redirect('gerenciar_midia')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")

            next_url = request.GET.get('next') or reverse('gerenciar_midia') # Correção: Usar request.GET para 'next'
            return redirect(next_url)
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'core/login.html', context)


# --- FUNÇÃO 5: Painel de Gerenciamento (URL /gerenciar/) ---
@login_required # Garante que só usuários logados acessem
def gerenciar_midia(request):
    """View para gerenciar mídias (upload com lógica cloud) e playlists."""

    if request.method == 'POST':
        form = MidiaForm(request.POST, request.FILES)

        if form.is_valid():
            midia_instance = form.save(commit=False)
            uploaded_file = midia_instance.arquivo_upload

            if uploaded_file:
                try:
                    url_gerada = cadastrarmidiaPcloud(uploaded_file, midia_instance.tipo)
                    if url_gerada:
                        midia_instance.url_publica = url_gerada
                        messages.success(request, 'Upload para Cloud e cadastro realizados com sucesso!')
                    else:
                        messages.error(request, '❌ Falha ao obter URL pública do Cloud.')
                        # Não salva se o URL falhar, apenas recarrega o form com erro
                        midias = Midia.objects.all().order_by('-data_upload')
                        context = {'midias': midias, 'form': form}
                        return render(request, 'core/painel_midia.html', context)

                except Exception as e:
                    messages.error(request, f'❌ Erro interno no Cloud: {e}')
                    # Re-renderiza o form com erro
                    midias = Midia.objects.all().order_by('-data_upload')
                    context = {'midias': midias, 'form': form}
                    return render(request, 'core/painel_midia.html', context)
            
            # Salva no banco de dados SE o URL foi gerado ou se não houve upload (mas URL manual válida)
            # Adicionar verificação se url_publica manual é permitida
            if midia_instance.url_publica or not uploaded_file:
                midia_instance.save() 
            else:
                 messages.error(request, 'Falha no upload ou URL pública ausente.') # Evita salvar sem URL
                 midias = Midia.objects.all().order_by('-data_upload')
                 context = {'midias': midias, 'form': form}
                 return render(request, 'core/painel_midia.html', context)


            # Lógica HTMX para atualização (se estiver usando)
            if request.headers.get('Hx-Request'):
                 midias = Midia.objects.all().order_by('-data_upload')
                 return render(request, 'core/partials/midia_list.html', {'midias': midias})

            return redirect(reverse('gerenciar_midia'))
        else:
            # Formulário inválido
            messages.error(request, 'Formulário inválido. Verifique os campos.')

    # Lógica GET (Exibir Formulário e Lista de Mídias)
    form = MidiaForm()
    midias = Midia.objects.all().order_by('-data_upload')

    context = {
        'midias': midias,
        'form': form,
        # Adicionar aqui a lógica para listar/editar playlists se necessário
    }

    return render(request, 'core/painel_midia.html', context)