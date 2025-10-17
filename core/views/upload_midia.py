import os
from django.shortcuts import render, redirect
from core.forms import UploadMidiaForm
from core.models.midia import Midia  # ajuste para seu modelo real
from django.utils import timezone

def upload_midia(request):
    if request.method == 'POST':
        form = UploadMidiaForm(request.POST, request.FILES)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            arquivo = form.cleaned_data['arquivo']
            caminho = f"midias/{arquivo.name}"

            # Salvar arquivo manualmente (opcional se usar MEDIA_ROOT automático)
            with open(os.path.join('media', arquivo.name), 'wb+') as destino:
                for chunk in arquivo.chunks():
                    destino.write(chunk)

            # Salvar no banco (ajuste os campos conforme seu modelo)
            midia = Midia(
                titulo=titulo,
                URL=caminho,
                Tipo_Midia_Id=1,  # ajuste conforme necessário
                Status='Ativo',
                Duracao=0,
                Data_Upload=timezone.now()
            )
            midia.save()

            return redirect('home')
    else:
        form = UploadMidiaForm()

    return render(request, 'core/upload_midia.html', {'form': form})
