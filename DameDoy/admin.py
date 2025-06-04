from django.contrib import admin
from .models import Material, PerfilUsuario, CarritoItem, Compra, DetalleCompra, Notificacion, Universidad, Facultad, Carrera, Materia, Docente

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'tipo', 'facultad', 'carrera', 'materia', 'precio', 'estado', 'fecha_publicacion')
    list_filter = ('estado', 'tipo', 'facultad', 'carrera', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion', 'autor__username', 'materia', 'docente', 'carrera', 'facultad')
    readonly_fields = ('fecha_publicacion', 'fecha_ultima_modificacion')
    list_editable = ('estado', 'precio')
    ordering = ('-fecha_publicacion',)
    date_hierarchy = 'fecha_publicacion'
    
    fieldsets = (
        ('Información Principal', {
            'fields': (
                 'titulo', 'tipo', 'descripcion', 'imagen' # 'archivo'
            )
        }),
        ('Detalles Académicos', {
            'fields': (
                'facultad', 'carrera', 'materia', 'docente'
            )
        }),
        ('Información de Publicación', {
            'fields': (
                'autor', 'precio', 'estado', 'motivo_rechazo'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_publicacion', 'fecha_ultima_modificacion'
            ),
            'classes': ('collapse',)
        }),
    )

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'genero', 'banco', 'fecha_registro')
    list_filter = ('genero', 'fecha_registro', 'banco')
    search_fields = ('usuario__username', 'usuario__email', 'telefono', 'direccion', 'banco')
    readonly_fields = ('fecha_registro',)
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': (
                'usuario', 'biografia'
            )
        }),
        ('Datos Personales', {
            'fields': (
                'telefono', 'direccion', 'fecha_nacimiento', 'genero'
            )
        }),
        ('Imágenes', {
            'fields': (
                'foto', 'foto_portada', 'qr_pago'
            )
        }),
        ('Información Bancaria', {
            'fields': (
                'banco', 'cuenta_banco'
            )
        }),
        ('Redes Sociales', {
            'fields': ('redes_sociales',),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'material', 'fecha_agregado')
    list_filter = ('fecha_agregado', 'usuario')
    search_fields = ('usuario__username', 'material__titulo')
    date_hierarchy = 'fecha_agregado'
    ordering = ('-fecha_agregado',)

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('codigo_seguimiento', 'usuario', 'total', 'estado', 'fecha_creacion', 'fecha_confirmacion')
    list_filter = ('estado', 'fecha_creacion', 'fecha_confirmacion', 'fecha_pago')
    search_fields = ('codigo_seguimiento', 'usuario__username', 'motivo_rechazo')
    readonly_fields = ('fecha_creacion', 'fecha_pago', 'fecha_confirmacion')
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Principal', {
            'fields': (
                'usuario', 'codigo_seguimiento', 'total', 'estado'
            )
        }),
        ('Detalles de Pago', {
            'fields': (
                'comprobante', 'motivo_rechazo'
            )
        }),
        # ('Materiales', {
        #     'fields': ('materiales',)
        # }),
        ('Fechas', {
            'fields': (
                'fecha_creacion', 'fecha_pago', 'fecha_confirmacion'
            ),
            'classes': ('collapse',)
        }),
    )

@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'material', 'precio_unitario', 'fecha_agregado')
    list_filter = ('fecha_agregado', 'compra__estado')
    search_fields = (
        'compra__codigo_seguimiento', 
        'material__titulo',
        'compra__usuario__username'
    )
    date_hierarchy = 'fecha_agregado'
    readonly_fields = ('fecha_agregado',)
    ordering = ('-fecha_agregado',)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = (
        'usuario', 
        'tipo', 
        'titulo', 
        'leida', 
        'fecha_creacion', 
        'referencia_tipo'
    )
    list_filter = (
        'tipo', 
        'leida', 
        'fecha_creacion',
        'referencia_tipo'
    )
    search_fields = (
        'usuario__username', 
        'titulo', 
        'mensaje',
        'referencia_id'
    )
    readonly_fields = ('fecha_creacion',)
    list_editable = ('leida',)
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Principal', {
            'fields': (
                'usuario', 'tipo', 'titulo', 'mensaje'
            )
        }),
        ('Estado', {
            'fields': ('leida',)
        }),
        ('Referencias', {
            'fields': (
                'referencia_tipo', 'referencia_id'
            )
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )

    actions = ['marcar_como_leidas', 'marcar_como_no_leidas']

    def marcar_como_leidas(self, request, queryset):
        queryset.update(leida=True)
    marcar_como_leidas.short_description = "Marcar notificaciones seleccionadas como leídas"

    def marcar_como_no_leidas(self, request, queryset):
        queryset.update(leida=False)
    marcar_como_no_leidas.short_description = "Marcar notificaciones seleccionadas como no leídas"

# Este código registra los modelos de la aplicación en el panel de administración de Django.
@admin.register(Universidad)
class UniversidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas', 'activo')
    search_fields = ('nombre', 'siglas')
    list_filter = ('activo',)

@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas', 'universidad', 'activo')
    search_fields = ('nombre', 'siglas')
    list_filter = ('universidad', 'activo')

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'facultad', 'activo')
    search_fields = ('nombre', 'codigo')
    list_filter = ('facultad__universidad', 'facultad', 'activo')

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'carrera', 'semestre', 'activo')
    search_fields = ('nombre', 'codigo')
    list_filter = ('carrera__facultad', 'carrera', 'semestre', 'activo')

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'universidad', 'facultad', 'carrera', 'materia', 'activo')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('activo', 'universidad', 'facultad', 'carrera', 'materia')
    ordering = ('apellido', 'nombre')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'email')
        }),
        ('Asignación Académica', {
            'fields': ('universidad', 'facultad', 'carrera', 'materia')
        }),
        ('Estado', {
            'fields': ('activo',)
        })
    )

    class Media:
        js = (
            'admin/js/docente_admin.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['facultad'].queryset = Facultad.objects.filter(universidad=obj.universidad)
            form.base_fields['carrera'].queryset = Carrera.objects.filter(facultad=obj.facultad)
            form.base_fields['materia'].queryset = Materia.objects.filter(carrera=obj.carrera)
        return form
