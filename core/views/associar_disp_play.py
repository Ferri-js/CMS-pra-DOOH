from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.template.loader import render_to_string
from core.models import Playlist, Dispositivo, Dispositivo_Playlist


@require_http_methods(["GET", "POST"])
def gerenciar_disp_play(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, idDispositivo=dispositivo_id)
    playlists = Playlist.objects.all().order_by('nomePlaylist')
    disp_play = Dispositivo_Playlist.objects.filter(
        id_dispositivo=dispositivo_id
    ).select_related('id_playlist').order_by('ordem_playlist')
    disps_plays_ids = list(disp_play.values_list('id_playlist', flat=True))

    if request.method == "POST":
        playlists_ids = request.POST.getlist('playlists')

        # valida duplicidades na ordem
        ordens = [int(v) for k, v in request.POST.items() if k.startswith('ordem_playlist')]
        if len(ordens) != len(set(ordens)):
            return HttpResponse("Erro: duas playlists não podem ter a mesma ordem!", status=400)

        # Cria associações novas, sem deletar existentes
        for play_id in playlists_ids:
            play = get_object_or_404(Playlist, idPlaylist=play_id)
            Dispositivo_Playlist.objects.get_or_create(id_dispositivo=dispositivo, id_playlist=play)

        # Atualiza ordem de exibição
        for dp in Dispositivo_Playlist.objects.filter(id_dispositivo=dispositivo):
            campo_nome = f"ordem_playlist_{dp.id_playlist.idPlaylist}"
            nova_ordem = request.POST.get(campo_nome)
            if nova_ordem:
                try:
                    dp.ordem_playlist = int(nova_ordem)
                    dp.save(update_fields=["ordem_playlist"])
                except ValueError:
                    pass

        # Atualiza lista de associações
        disps_playlists = Dispositivo_Playlist.objects.filter(
            id_dispositivo=dispositivo
        ).select_related('id_playlist').order_by('ordem_playlist')

        # ⚡ Se for uma requisição HTMX, retorna só o parcial
        if request.headers.get('HX-Request'):
            html = render_to_string(
                "core/partials/disp_playlist.html",  # o mesmo nome do seu include
                {"disps_playlists": disps_playlists}
            )
            return HttpResponse(html)

        # Caso não seja HTMX, renderiza a página inteira
        context = {
            'disp': dispositivo,
            'playlists': playlists,
            'disps_playlists': disps_playlists,
            'disps_playlists_ids': disps_plays_ids,
        }
        return render(request, 'core/painel_associar_disp_play.html', context)

    # GET normal
    context = {
        'disp': dispositivo,
        'playlists': playlists,
        'disps_playlists': disp_play,
        'disps_playlists_ids': disps_plays_ids,
    }
    return render(request, 'core/painel_associar_disp_play.html', context)
