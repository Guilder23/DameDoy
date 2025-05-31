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
]
