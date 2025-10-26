from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Midia, Playlist, ItemPlaylist, Dispositivo, TipoDispositivo
from .forms import MidiaForm, LoginForm
import time

# --- FUNÇÃO DE UPLOAD PARA O CLOUD (SIMULAÇÃO) ---
def cadastrarmidiaPcloud(arquivo_django, tipo_midia):
    print(f"--- INICIANDO UPLOAD PARA CLOUD: {arquivo_django.name} ({tipo_midia}) ---")
    time.sleep(0.5) 
    url_gerada = f"https://seuservidorcloud.com/midias/{arquivo_django.name.replace(' ', '_')}"
    print(f"--- UPLOAD CONCLUÍDO. URL GERADO: {url_gerada} ---")
    return url_gerada
# -------------------------------------------------------------


# --- FUNÇÃO 1: Home Page / Dashboard (URL '/') ---
def home(request):
    return render(request, 'core/home.html', {})


# --- FUNÇÃO 2: TELA DE VERIFICAÇÃO (URL /verificar/) ---
def tela_verificacao(request):
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo_verificacao')
        
        try:
            dispositivo = Dispositivo.objects.get(codVerificacao=codigo)
            
            request.session['dispositivo_id'] = dispositivo.pk
            messages.success(request, f"Dispositivo {dispositivo.nomeDispositivo} autorizado!")
            return redirect('player_exibicao')
            
        except Dispositivo.DoesNotExist:
            messages.error(request, "Código de verificação inválido ou dispositivo não encontrado.")
            
    return render(request, 'core/verificacao.html', {})


# --- FUNÇÃO 3: Player de Exibição em Loop (URL /exibir/) ---
def player_exibicao(request):
    
    if 'dispositivo_id' not in request.session:
        return redirect('verificacao') 

    playlist = Playlist.objects.filter(ativa=True).prefetch_related('itens__midia').first()
    
    context = {
        'playlist': playlist
    }
    
    return render(request, 'core/player_loop.html', context)


# --- FUNÇÃO 4: TELA DE LOGIN CUSTOMIZADA (URL /login/) ---
def tela_login(request):
    
    if request.user.is_authenticated:
        return redirect('gerenciar_midia')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST) 
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.username}!")
            
            next_url = request.POST.get('next') or reverse('gerenciar_midia')
            return redirect(next_url) 
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    else:
        form = LoginForm() 
        
    context = {'form': form}
    return render(request, 'core/login.html', context)


# --- FUNÇÃO 5: Painel de Gerenciamento (URL /gerenciar/) ---
@login_required 
def gerenciar_midia(request):

    if request.method == 'POST':
        form = MidiaForm(request.POST, request.FILES) 
        
        if form.is_valid():
            midia_instance = form.save(commit=False) 
            uploaded_file = midia_instance.arquivo_upload
            
            if uploaded_file:
                url_gerada = cadastrarmidiaPcloud(uploaded_file, midia_instance.tipo) 
                midia_instance.url_publica = url_gerada
            
            midia_instance.save() 
            
            if request.headers.get('Hx-Request'):
                 midias = Midia.objects.all().order_by('-data_upload')
                 return render(request, 'core/partials/midia_list.html', {'midias': midias})
            
            return redirect(reverse('gerenciar_midia'))
        else:
            messages.error(request, 'Formulário inválido. Verifique os campos.')

    form = MidiaForm() 
    midias = Midia.objects.all().order_by('-data_upload')

    context = {
        'midias': midias,
        'form': form,
    }
    
    return render(request, 'core/painel_midia.html', context)