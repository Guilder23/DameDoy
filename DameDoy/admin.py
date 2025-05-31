from django.contrib import admin
from .models import Material, PerfilUsuario

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'tipo', 'facultad', 'carrera', 'materia', 'precio', 'estado', 'fecha_publicacion')
    list_filter = ('estado', 'tipo', 'facultad', 'carrera')
    search_fields = ('titulo', 'descripcion', 'autor__username', 'materia', 'docente')
    readonly_fields = ('fecha_publicacion', 'fecha_ultima_modificacion')
    list_editable = ('estado', 'precio')
    ordering = ('-fecha_publicacion',)
    date_hierarchy = 'fecha_publicacion'
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'tipo', 'descripcion', 'imagen')
        }),
        ('Detalles Académicos', {
            'fields': ('facultad', 'carrera', 'materia', 'docente')
        }),
        ('Información de Publicación', {
            'fields': ('autor', 'precio', 'estado', 'motivo_rechazo')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion', 'fecha_ultima_modificacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'genero', 'fecha_registro')
    list_filter = ('genero', 'fecha_registro')
    search_fields = ('usuario__username', 'usuario__email', 'telefono', 'direccion')
    readonly_fields = ('fecha_registro',)
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario', 'biografia')
        }),
        ('Datos Personales', {
            'fields': ('telefono', 'direccion', 'fecha_nacimiento', 'genero')
        }),
        ('Imágenes', {
            'fields': ('foto', 'foto_portada')
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
