from django.urls import path
from .views import home
from core.views.teste_frontend import teste_frontend 
from core.views.upload_midia import upload_midia

urlpatterns = [
      path('', home, name='home'),
      path('teste_frontend/', teste_frontend, name='teste_frontend'),
      path('upload/', upload_midia, name='upload_midia'),
]
