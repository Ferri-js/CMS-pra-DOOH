from django.shortcuts import render, get_object_or_404
from core.models.playlist import Playlist
from core.models.midia_playlist import Midia_Playlist
from core.models.dispositivo import Dispositivo
from core.models.disp_playlist import Dispositivo_Playlist

def player_view(request, codigo):
    dispositivo = get_object_or_404(Dispositivo, codVerificacao=codigo)

    # Pega as playlists associadas ao dispositivo, na ordem correta
    disp_playlists = Dispositivo_Playlist.objects.filter(
        id_dispositivo=dispositivo
    ).select_related('id_playlist').order_by('ordem_playlist')

    midias = []

    # Para cada playlist, pega as mídias na ordem certa
    for disp_playlist in disp_playlists:
        playlist = disp_playlist.id_playlist
        midia_playlists = Midia_Playlist.objects.filter(
            id_playlist=playlist
        ).select_related('id_midia__tipo_midia').order_by('ordem_midia')

        midias.extend([mp.id_midia for mp in midia_playlists])

    return render(request, 'core/player.html', {
        'dispositivo': dispositivo,
        'midias': midias
    })
