from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.template.loader import render_to_string
from core.models import Playlist, Midia, Midia_Playlist

@require_http_methods(["GET", "POST"])
def gerenciar_mp(request, playlist_id):
    playlist = get_object_or_404(Playlist, idPlaylist=playlist_id)
    midias = Midia.objects.all().order_by('titulo')
    midias_playlist = Midia_Playlist.objects.filter(id_playlist=playlist).select_related('id_midia').order_by('ordem_midia')
    midias_associadas_ids = list(midias_playlist.values_list('id_midia', flat=True))

    if request.method == "POST":
        midia_ids = request.POST.getlist('midias')

        ordens = [int(v) for k, v in request.POST.items() if k.startswith('ordem_midia')]
        if len(ordens) != len(set(ordens)):
            # Há duplicidade
            return HttpResponse("Erro: duas mídias não podem ter a mesma ordem!", status=400)

        # Cria associações novas, sem deletar existentes
        for midia_id in midia_ids:
            midia = get_object_or_404(Midia, id=midia_id)
            Midia_Playlist.objects.get_or_create(id_playlist=playlist, id_midia=midia)

        # Atualiza ordem de exibição
        for mp in Midia_Playlist.objects.filter(id_playlist=playlist):
            campo_nome = f"ordem_midia_{mp.id_midia.id}"
            nova_ordem = request.POST.get(campo_nome)
            if nova_ordem:
                try:
                    mp.ordem_midia = int(nova_ordem)
                    #mp.save(update_fields=["ordem_midia"])
                    mp.associarMP()
                except ValueError:
                    pass

        midias_playlist = Midia_Playlist.objects.filter(id_playlist=playlist).select_related('id_midia').order_by('ordem_midia')
        html = render_to_string("core/partials/midia_playlist_list.html", {"midias_playlist": midias_playlist})
        return HttpResponse(html)

    context = {
        'playlist': playlist,
        'midias': midias,
        'midias_playlist': midias_playlist,
        'midias_associadas_ids': midias_associadas_ids,
    }
    return render(request, 'core/painel_associar_mp.html', context)
