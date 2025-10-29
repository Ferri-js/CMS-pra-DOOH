from django import forms
from .models import Midia, Playlist, Midia_Playlist, Dispositivo

# core/forms.py
class MidiaForm(forms.ModelForm):
    class Meta:
        model = Midia
        # Mude de 'url' para 'arquivo_upload'
        fields = ['titulo', 'tipo_midia', 'arquivo_upload', 'duracao'] 
        # ...

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['nomePlaylist']

        labels = {
            'nomePlaylist': 'Titulo da Playlist',
        }

class MidiaPlaylistForm(forms.ModelForm):
    class Meta:
        model = Midia_Playlist
        fields = []        

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['nomeDispositivo', 'tipoDispositivo', 'codVerificacao']

        labels = {
            'nomeDispositivo': 'Nome do Dispositivo',
            'tipoDispositivo': 'Tipo do Dispositivo',
            'codVerificacao': 'Codigo de verificacao do Dispositvo',
        }


#class UploadMidiaForm(forms.Form):
#    titulo = forms.CharField(max_length=255, required=True)
#    arquivo = forms.FileField(required=True)        