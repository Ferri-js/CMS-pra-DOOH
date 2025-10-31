# core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
# ⚠️ IMPORTANTE: Assumindo que seus models estão em 'core/models.py'
from .models import Midia, Playlist, ItemPlaylist, Dispositivo, TipoDispositivo

# --- Formulário para Login Visual ---
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Nome de Usuário', 
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Senha', 
            'class': 'form-control'
        })

# --- Formulário para Upload de Mídia ---
class MidiaForm(forms.ModelForm):
    class Meta:
        model = Midia
        # O usuário não preenche a 'url_publica' se 'arquivo_upload' for usado
        fields = ['titulo', 'tipo', 'arquivo_upload', 'duracao', 'url_publica']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da Mídia'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'arquivo_upload': forms.FileInput(attrs={'class': 'form-control'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duração (seg.) (só para imagens)'}),
            'url_publica': forms.URLInput(attrs={'class': 'form-control', 'placeholder': '(Opcional) Cole um URL externo (para tipo HTML)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Nenhum campo é obrigatório por padrão, a view fará a validação
        self.fields['arquivo_upload'].required = False
        self.fields['url_publica'].required = False
        self.fields['duracao'].required = False
        self.fields['titulo'].required = True
        self.fields['tipo'].required = True

# --- Formulário para Criar Playlist ---
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['titulo', 'ativa']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Nome da nova playlist', 'class': 'form-control'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# --- Formulário para Adicionar Item à Playlist ---
class ItemPlaylistForm(forms.ModelForm):
    midia = forms.ModelChoiceField(
        queryset=Midia.objects.all(), # A view vai filtrar pelas mídias corretas
        label="Mídia",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = ItemPlaylist
        fields = ['midia', 'ordem']
        widgets = {
            'ordem': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ordem (ex: 10, 20)'})
        }

# --- Formulário para Criar/Editar Dispositivo ---
class DispositivoForm(forms.ModelForm):
    # Campos que precisam de querysets dinâmicos
    playlistAssociada = forms.ModelChoiceField(
        queryset=Playlist.objects.all(),
        required=False, # Um dispositivo pode não ter playlist
        label="Playlist Associada",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipoDispositivo = forms.ModelChoiceField(
        queryset=TipoDispositivo.objects.all(),
        required=True,
        label="Tipo de Dispositivo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Dispositivo
        fields = ['nomeDispositivo', 'codVerificacao', 'status', 'tipoDispositivo', 'playlistAssociada']
        widgets = {
            'nomeDispositivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome (ex: TV da Sala)'}),
            'codVerificacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código (ex: 12345)'}),
            'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Status (ex: ativo)'}), 
        }