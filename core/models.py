from django.db import models
# core/models.py

class Material(models.Model):
    # Definimos los tipos de material (Crítico o Interno)
    TIPO_CHOICES = [
        ('critico', 'Material Crítico'),
        ('interno', 'Material Interno'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad = models.IntegerField(default=0)
   
    imagen = models.ImageField(upload_to='materiales/', null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='interno')

    def __str__(self):
        return self.nombre
