from django import forms
from .models import Midia 
from django.contrib.auth.forms import AuthenticationForm

# core/forms.py
class MidiaForm(forms.ModelForm):
    class Meta:
        model = Midia
        # Mude de 'url' para 'arquivo_upload'
        fields = ['titulo', 'tipo', 'arquivo_upload', 'duracao'] 
        # ...

class LoginForm(AuthenticationForm):
    """
    Formulário customizado para login. Herda do formulário de autenticação do Django.
    """
    # Exemplo opcional de personalização visual no VS Code
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta os placeholders para melhor usabilidade
        self.fields['username'].widget.attrs.update({'placeholder': 'Nome de Usuário ou E-mail'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Senha'})

    pass