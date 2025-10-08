from django import forms
from .models import Midia 

class MidiaForm(forms.ModelForm):
    """Formulário usado no painel de gerenciamento para criar/editar mídias."""
    class Meta:
        model = Midia
        # Inclua os campos que o usuário pode preencher
        fields = ['titulo', 'tipo', 'url', 'duracao'] 
        
        # Opcional: Adicionar estilos básicos (você pode customizar o 'input-field' no CSS)
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-field'}),
            'tipo': forms.TextInput(attrs={'class': 'input-field'}),
            'url': forms.URLInput(attrs={'class': 'input-field'}),
            'duracao': forms.NumberInput(attrs={'class': 'input-field'}),
        }