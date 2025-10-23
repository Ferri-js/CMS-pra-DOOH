from django import forms
from .models import Midia 

# core/forms.py
class MidiaForm(forms.ModelForm):
    class Meta:
        model = Midia
        # Mude de 'url' para 'arquivo_upload'
        fields = ['titulo', 'tipo_midia', 'arquivo_upload', 'duracao'] 
        # ...

#class UploadMidiaForm(forms.Form):
#    titulo = forms.CharField(max_length=255, required=True)
#    arquivo = forms.FileField(required=True)        