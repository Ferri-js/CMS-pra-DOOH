from django.contrib import admin
from django.urls import path, include  # ⬅️ Certifique-se de que 'include' está aqui
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Rota para o Admin do Django
    path('admin/', admin.site.urls),
    
    # 2. Inclui TODAS as URLs definidas em 'core/urls.py'
    # Esta linha direciona tudo para o seu app 'core'
    path('', include('core.urls')), 
]

# ⬇️ Esta parte é importante para o upload de mídia funcionar no modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# ❌ REMOVA QUALQUER LINHA COMO "from . import views" DESTE ARQUIVO! ❌