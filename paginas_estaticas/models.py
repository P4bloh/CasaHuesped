from django.db import models

# Create your models here.
class PaginaInicio(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()