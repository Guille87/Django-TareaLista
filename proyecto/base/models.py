from django.db import models
from django.contrib.auth.models import User


# Modelo que representa una tarea en la aplicación
class Tarea(models.Model):
    # Relación con el modelo de usuario de Django
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,
                                null=True,  # El usuario puede ser nulo si la tarea no está asignada
                                blank=True)  # El campo puede dejarse en blanco
    titulo = models.CharField(max_length=200)  # Título de la tarea
    descripcion = models.TextField(null=True,  # La descripción puede ser nula
                                   blank=True)  # El campo puede dejarse en blanco
    completo = models.BooleanField(default=False)  # Estado de completitud de la tarea
    creado = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación de la tarea
    completado = models.DateTimeField(null=True, blank=True)  # Fecha y hora de la tarea completada

    def __str__(self):
        """
        Devuelve una representación legible de la tarea en el administrador de Django y otros lugares.
        """
        return self.titulo

    class Meta:
        """
        Clase Meta para configurar opciones adicionales del modelo.
        """
        ordering = ['completo']  # Ordenar las tareas por su estado de completitud

