from django import forms
from .models import Midia 

# core/forms.py
class MidiaForm(forms.ModelForm):
    class Meta:
        model = Midia
        # Mude de 'url' para 'arquivo_upload'
        fields = ['titulo', 'tipo', 'arquivo_upload', 'duracao'] 
        # ...