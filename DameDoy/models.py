from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError  # Agregar esta línea

class Universidad(models.Model):
    nombre = models.CharField(max_length=200)
    siglas = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Universidad"
        verbose_name_plural = "Universidades"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.siglas} - {self.nombre}"

class Facultad(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name='facultades')
    nombre = models.CharField(max_length=200)
    siglas = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"
        unique_together = ['universidad', 'siglas']
        ordering = ['universidad', 'nombre']

    def __str__(self):
        return f"{self.universidad.siglas} - {self.siglas} - {self.nombre}"

class Carrera(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name='carreras')
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='carreras')
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        unique_together = ['universidad', 'facultad', 'codigo']
        ordering = ['universidad', 'facultad', 'nombre']

    def __str__(self):
        return f"{self.universidad.siglas} - {self.facultad.siglas} - {self.codigo} - {self.nombre}"

    def clean(self):
        if self.facultad.universidad != self.universidad:
            raise ValidationError('La facultad debe pertenecer a la universidad seleccionada')

class Materia(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name='materias')
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='materias')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='materias')
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20)
    semestre = models.IntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        unique_together = ['universidad', 'facultad', 'carrera', 'codigo']
        ordering = ['universidad', 'facultad', 'carrera', 'semestre', 'nombre']

    def __str__(self):
        return f"{self.universidad.siglas} - {self.carrera.codigo} - {self.codigo} - {self.nombre}"

    def clean(self):
        if self.carrera.facultad != self.facultad or self.carrera.universidad != self.universidad:
            raise ValidationError('La carrera debe pertenecer a la facultad y universidad seleccionadas')

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"
        ordering = ['apellido', 'nombre']  # Ordenamiento simple
        unique_together = ['universidad', 'facultad', 'carrera', 'materia', 'email']

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.materia}"

    def clean(self):
        if self.facultad and self.facultad.universidad != self.universidad:
            raise ValidationError('La facultad debe pertenecer a la universidad seleccionada')
        if self.carrera and (self.carrera.facultad != self.facultad or 
                           self.carrera.universidad != self.universidad):
            raise ValidationError('La carrera debe pertenecer a la facultad y universidad seleccionadas')
        if self.materia and (self.materia.carrera != self.carrera or 
                          self.materia.facultad != self.facultad or 
                          self.materia.universidad != self.universidad):
            raise ValidationError('La materia debe pertenecer a la carrera, facultad y universidad seleccionadas')

class Material(models.Model):
    TIPO_MATERIAL = [
        ('apunte', 'Apunte'),
        ('examen', 'Examen'),
        ('proyecto', 'Proyecto'),
        ('libro', 'Libro'),
        ('otros', 'Otros'),
    ]

    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('pendiente', 'Pendiente de revisión'),
        ('publicado', 'Publicado'),
        ('rechazado', 'Rechazado'),
        ('archivado', 'Archivado'),
        ('eliminado', 'Eliminado'),
        ('suspendido', 'Suspendido'),
        ('vendido', 'Vendido/No disponible'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título", null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_MATERIAL, verbose_name="Tipo de Material", null=True, blank=True)
    universidad = models.ForeignKey(Universidad, on_delete=models.SET_NULL, null=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.SET_NULL, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True)
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(verbose_name="Descripción", null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    imagen = models.ImageField(upload_to='materiales/', null=True, blank=True, verbose_name="Imagen (opcional)")
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES,
        default='borrador',
        verbose_name="Estado"
    )
    motivo_rechazo = models.TextField(
        null=True, 
        blank=True,
        verbose_name="Motivo de rechazo"
    )
    fecha_ultima_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última modificación"
    )

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
    qr_pago = models.ImageField(
        upload_to='qr_pagos/', 
        null=True, 
        blank=True,
        verbose_name="QR para pagos"
    )
    cuenta_banco = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name="Número de cuenta bancaria"
    )
    banco = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name="Nombre del banco"
    )
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)
#Carrito de Compras-------------------------------------------------
class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_agregado']
        unique_together = ['usuario', 'material']

    def __str__(self):
        return f"{self.usuario.username} - {self.material.titulo}"
#Compra y Detalle de Compra-------------------------------------------------
class Compra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pagado y en revisión'),
        ('confirmado', 'Pago confirmado'),
        ('rechazado', 'Pago rechazado'),
        ('cancelado', 'Compra cancelada')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
    materiales = models.ManyToManyField(Material, through='DetalleCompra')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    comprobante = models.ImageField(upload_to='comprobantes/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    motivo_rechazo = models.TextField(null=True, blank=True)
    codigo_seguimiento = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_agregado']

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('pago_recibido', 'Pago Recibido'),
        ('pago_confirmado', 'Pago Confirmado'),
        ('pago_rechazado', 'Pago Rechazado'),
        ('compra_realizada', 'Compra Realizada'),
        ('material_vendido', 'Material Vendido'),
        ('material_publicado', 'Material Publicado'),
        ('material_rechazado', 'Material Rechazado')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    referencia_id = models.IntegerField(null=True, blank=True)  # ID de la compra o material relacionado
    referencia_tipo = models.CharField(max_length=50, null=True, blank=True)  # 'compra' o 'material'

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo}"

    def marcar_como_leida(self):
        self.leida = True
        self.save()

    def get_imagen_url(self):
        """Obtener la URL de la imagen relacionada con la notificación"""
        if self.referencia_tipo == 'compra':
            try:
                compra = Compra.objects.get(id=self.referencia_id)
                if compra.comprobante:
                    return compra.comprobante.url
                # Si no hay comprobante, mostrar la imagen del primer material
                primer_material = compra.materiales.first()
                if primer_material and primer_material.imagen:
                    return primer_material.imagen.url
            except Compra.DoesNotExist:
                pass
        return None  # O una URL de imagen por defecto
    
    @property
    def compra(self):
        if self.referencia_tipo == 'compra':
            try:
                return Compra.objects.get(id=self.referencia_id)
            except Compra.DoesNotExist:
                return None
        return None

