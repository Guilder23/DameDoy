from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Material(models.Model):
    TIPO_MATERIAL = [
        ('apunte', 'Apunte'),
        ('examen', 'Examen'),
        ('proyecto', 'Proyecto'),
        ('libro', 'Libro'),
        ('otros', 'Otros'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título", null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_MATERIAL, verbose_name="Tipo de Material", null=True, blank=True)
    facultad = models.CharField(max_length=100, verbose_name="Facultad", null=True, blank=True)
    carrera = models.CharField(max_length=100, verbose_name="Carrera", null=True, blank=True)
    materia = models.CharField(max_length=100, verbose_name="Materia", null=True, blank=True)
    docente = models.CharField(max_length=100, verbose_name="Nombre del Docente", null=True, blank=True)
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    imagen = models.ImageField(upload_to='materiales/', null=True, blank=True, verbose_name="Imagen (opcional)")

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

    def __str__(self):
        return f"{self.titulo} - {self.materia} ({self.tipo})"

class PerfilUsuario(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_portada = models.ImageField(upload_to='portadas/', null=True, blank=True)
    foto = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)
    redes_sociales = models.JSONField(default=dict, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)
