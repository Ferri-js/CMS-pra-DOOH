# core/models/tipoDispositivo.py
from django.db import models

class TipoDispositivo(models.Model):
    # O Django gerencia o ID automaticamente
    nome = models.CharField(max_length=255, verbose_name="Nome do Tipo")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name_plural = 'Tipos de Dispositivo'
        # O Django agora CRIA esta tabela no SQLite
        # managed = True (comportamento padrão)