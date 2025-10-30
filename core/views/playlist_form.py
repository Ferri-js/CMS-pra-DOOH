
from django.shortcuts import render, redirect
from django.urls import reverse
from core.models import Playlist
from core.forms import PlaylistForm


def gerenciar_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)

        if form.is_valid():
            play_instance = form.save(commit=False)
            #play_instance.save()
            play_instance.cadastrarPlaylistORM()

            if request.headers.get('Hx-Request'):
                playlists = Playlist.objects.all().order_by('-idPlaylist')
                return render(request, 'core/partials/playlist_list.html', {'playlists': playlists})

            return redirect(reverse('gerenciar_play'))
        else:
            # Mostra os erros no console e passa para o template
            print(form.errors)

    else:
        form = PlaylistForm()

    playlists = Playlist.objects.all().order_by('-idPlaylist')
    return render(request, 'core/painel_playlist.html', {
        'playlists': playlists,
        'form': form,
        'form_errors': form.errors if request.method == 'POST' else None
    })
