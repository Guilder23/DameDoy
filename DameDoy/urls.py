from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('html/registro/', views.registro, name='registro'),
    path('html/login/', views.login_view, name='login'),
    path('html/logout/', views.logout_view, name='logout'),
    #path('html/materiales/', views.lista_materiales, name='materiales'),
    path('html/materiales/', views.lista_materiales, name='lista_materiales'),
    path('html/publicar/', views.publicar_material, name='publicar_material'),
    path('html/perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('actualizar-imagen/', views.actualizar_imagen, name='actualizar_imagen'),

    path('html/mis-materiales/', views.mis_materiales, name='mis_materiales'),
    path('html/material/<int:pk>/editar/', views.editar_material, name='editar_material'),
    path('html/material/<int:pk>/estado/', views.cambiar_estado_material, name='cambiar_estado_material'),
    path('html/material/<int:pk>/eliminar/', views.eliminar_material, name='eliminar_material'),

    # Agregar a urlpatterns
    path('carrito/agregar/<int:material_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/obtener/', views.obtener_carrito, name='obtener_carrito'),
    path('carrito/eliminar/<int:material_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path('compra/', views.vista_compra, name='vista_compra'),
    path('compra/procesar/', views.procesar_compra, name='procesar_compra'),
    path('compra/cancelar/', views.cancelar_compra, name='cancelar_compra'),
    
    # Notificaciones
    path('notificaciones/recientes/', views.notificaciones_recientes, name='notificaciones_recientes'),
    path('notificaciones/marcar-leidas/', views.marcar_notificaciones_leidas, name='marcar_notificaciones_leidas'),
    path('notificaciones/todas/', views.todas_notificaciones, name='todas_notificaciones'),
    path('verificar-pago/<int:compra_id>/', views.verificar_pago, name='verificar_pago'),

    path('mis-compras/', views.mis_compras, name='mis_compras'),
]
