from django.db import models
from django.contrib.auth.models import User

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): return self.nombre

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class SesionPomodoro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    duracion_minutos = models.IntegerField(default=25)
    fecha = models.DateTimeField(auto_now_add=True)