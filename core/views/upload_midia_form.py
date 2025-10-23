import uuid
import time
from django.shortcuts import render, redirect
from django.urls import reverse
from core.models import Midia, Playlist
from core.forms import MidiaForm
from supabase import create_client


# --- FUNÇÃO DE UPLOAD PARA O CLOUD (SIMULAÇÃO) ---
def cadastrarMidiaSupabase(arquivo_enviado):
    """Função que simula o envio para a Nuvem e retorna o URL público."""
    print(f"--- INICIANDO UPLOAD PARA CLOUD: {arquivo_enviado.name} ---")
    #time.sleep(0.5)

    nome_bucket = "NexxoMedias"
    pasta_bucket = "medias"
    SUPABASE_URL="https://tvrvftpiozxlubejbzmu.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2cnZmdHBpb3p4bHViZWpiem11Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA4NDk5NjgsImV4cCI6MjA3NjQyNTk2OH0.itPIuGqmk9QTpj9cJMeQqeIRIZpoKDH8AUIfvNsu1Qk"

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    nome_bucket = "NexxoMedias"
    pasta_bucket = "medias"
    
    # cria nome único para o arquivo
    caminho_arquivo = f"{pasta_bucket}/{uuid.uuid4().hex}_{arquivo_enviado.name}"
    
    # envia os bytes do arquivo diretamente (não usar content_type)
    supabase.storage.from_(nome_bucket).upload(
        caminho_arquivo,
        arquivo_enviado.read()
    )
    
    # retorna URL pública
    url = supabase.storage.from_(nome_bucket).get_public_url(caminho_arquivo)
    return url


# --- FUNÇÃO 2: Painel de Gerenciamento Visual (URL /gerenciar/) ---
def gerenciar_midia(request):
    if request.method == 'POST':
        form = MidiaForm(request.POST)
        arquivo = request.FILES.get('arquivo_upload')  # pega arquivo do POST

        if form.is_valid():
            midia_instance = form.save(commit=False)

            if arquivo:
                url_gerada = cadastrarMidiaSupabase(arquivo)
                midia_instance.url = url_gerada  # salva apenas URL no banco

            midia_instance.save()

            if request.headers.get('Hx-Request'):
                midias = Midia.objects.all().order_by('-data_upload')
                return render(request, 'core/partials/midia_list.html', {'midias': midias})

            return redirect(reverse('gerenciar_midia'))
        else:
            # Mostra os erros no console e passa para o template
            print(form.errors)

    else:
        form = MidiaForm()

    midias = Midia.objects.all().order_by('-data_upload')
    return render(request, 'core/painel_midia.html', {
        'midias': midias,
        'form': form,
        'form_errors': form.errors if request.method == 'POST' else None
    })
