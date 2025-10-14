import os
import django
from datetime import datetime
from django.utils import timezone
# Configure o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexxo_cms.settings')  # Substitua corretamente
django.setup()

# Agora os imports funcionam como em qualquer lugar do projeto
from core.models.tipoMidia import tipoFormato
from core.models.midia import Midia

tipo = tipoFormato.objects.get(id=1)

midia = Midia(
    titulo="Teste direto do script",
    tipo_midia=tipo,
    url="http://exemplo.com/script",
    status="ativo",
    duracao=90,
    data_upload=timezone.now()
)

midia.cadastrarMidia()

print(f"Mídia criada/atualizada com ID: {midia.id}")
