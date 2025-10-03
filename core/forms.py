from django import forms

class UploadMidiaForm(forms.Form):
    titulo = forms.CharField(max_length=255, required=True)
    arquivo = forms.FileField(required=True)
