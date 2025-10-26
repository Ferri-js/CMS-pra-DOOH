# core/models/dispositivo.py
from django.db import models
from .tipoDispositivo import TipoDispositivo
from .playlist import Playlist # Assumindo que este Model está correto

class Dispositivo(models.Model):
    nomeDispositivo = models.CharField(max_length=255, verbose_name="Nome")
    codVerificacao = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Código de Verificação"
    )
    status = models.IntegerField(null=True, blank=True)

    # Relações limpas (ForeignKey)
    tipoDispositivo = models.ForeignKey(
        TipoDispositivo, 
        on_delete=models.SET_NULL, 
        null=True
    )
    playlistAssociada = models.ForeignKey(
        Playlist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Playlist Ativa"
    )

    def __str__(self):
        return self.nomeDispositivo
    
    class Meta:
        verbose_name_plural = 'Dispositivos'
        # managed = True (O Django CRIARÁ esta tabela)