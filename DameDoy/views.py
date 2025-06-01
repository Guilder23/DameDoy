from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Material, PerfilUsuario, CarritoItem, Compra, DetalleCompra, Notificacion  # Quitamos Facultad
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth
from .forms import MaterialForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import uuid
from django.utils.timesince import timesince


@login_required
def inicio(request):
    return render(request, 'html/inicio.html')

def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('login')
    return render(request, 'html/registro.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            messages.success(request, '¡Has iniciado sesión correctamente!')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'html/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#MOSTRAR MATERIALES---------------------------------------------------------
@login_required
def publicar_material(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)

    # Verificar si el perfil está completo
    campos_obligatorios = [
        request.user.first_name,
        request.user.last_name,
        request.user.email,
        perfil.telefono,
        perfil.direccion,
        perfil.fecha_nacimiento,
        perfil.genero
    ]

    if not all(campos_obligatorios):
        messages.warning(request, 'Debes completar tu perfil antes de publicar un material.')
        return redirect('perfil_usuario')

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.autor = request.user
            material.estado = 'pendiente'  # Establecer estado inicial como pendiente
            material.save()
            messages.success(request, f'¡Material enviado para revisión! {material.titulo}')
            return redirect('mis_materiales')  # Redirigir a mis materiales para ver el estado
    else:
        form = MaterialForm()
    
    return render(request, 'html/publicar_material.html', {'form': form})


def lista_materiales(request):
    materiales = Material.objects.all()
    materiales = Material.objects.filter(estado__in=['publicado', 'vendido'])
    # Búsqueda
    query = request.GET.get('q')
    if query:
        materiales = materiales.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(materia__icontains=query) |
            Q(facultad__icontains=query) |
            Q(carrera__icontains=query)
        )
    
    # Filtros
    tipo = request.GET.get('tipo')
    facultad = request.GET.get('facultad')
    carrera = request.GET.get('carrera')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    
    if tipo:
        materiales = materiales.filter(tipo=tipo)
    if facultad:
        materiales = materiales.filter(facultad__icontains=facultad)
    if carrera:
        materiales = materiales.filter(carrera__icontains=carrera)
    if precio_min:
        materiales = materiales.filter(precio__gte=precio_min)
    if precio_max:
        materiales = materiales.filter(precio__lte=precio_max)
    
    # Obtener valores únicos para los filtros directamente de los materiales
    facultades = Material.objects.values_list('facultad', flat=True).distinct()
    carreras = Material.objects.values_list('carrera', flat=True).distinct()
    
    context = {
        'materiales': materiales,
        'tipos': Material.TIPO_MATERIAL,
        'facultades': facultades,
        'carreras': carreras,
        'filtros_actuales': request.GET,
    }
    return render(request, 'html/materiales.html', context)

@login_required
def perfil_usuario(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Actualizar datos del perfil
        perfil.telefono = request.POST.get('telefono', '')
        perfil.biografia = request.POST.get('biografia', '')
        perfil.direccion = request.POST.get('direccion', '')
        perfil.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        perfil.genero = request.POST.get('genero', '')
        
        # Manejar redes sociales
        redes_sociales = {
            'facebook': request.POST.get('facebook', ''),
            'twitter': request.POST.get('twitter', ''),
            'instagram': request.POST.get('instagram', ''),
            'linkedin': request.POST.get('linkedin', '')
        }
        perfil.redes_sociales = redes_sociales
        
        # Manejar fotos
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
        if 'foto_portada' in request.FILES:
            perfil.foto_portada = request.FILES['foto_portada']
        
        # Actualizar datos de pago
        perfil.banco = request.POST.get('banco', '')
        perfil.cuenta_banco = request.POST.get('cuenta_banco', '')
        
        # Manejar archivo QR
        if 'qr_pago' in request.FILES:
            perfil.qr_pago = request.FILES['qr_pago']
        
        perfil.save()
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('perfil_usuario')
    
    return render(request, 'html/perfil_usuario.html', {'perfil': perfil})

@require_POST
@login_required
def actualizar_imagen(request):
    try:
        perfil = request.user.perfilusuario
        tipo = request.POST.get('tipo')
        
        if tipo == 'foto' and 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
        elif tipo == 'foto_portada' and 'foto_portada' in request.FILES:
            perfil.foto_portada = request.FILES['foto_portada']
        
        perfil.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def mis_materiales(request):
    materiales = Material.objects.filter(autor=request.user).order_by('-fecha_publicacion')
    
    context = {
        'materiales': materiales,
        'estados': Material.ESTADO_CHOICES,
    }
    return render(request, 'html/mis_materiales.html', context)

@login_required
def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            material = form.save(commit=False)
            # Si se cambia algo, volver a estado pendiente
            if material.estado == 'publicado':
                material.estado = 'pendiente'
            material.save()
            messages.success(request, 'Material actualizado exitosamente')
            return redirect('mis_materiales')
    else:
        form = MaterialForm(instance=material)
    
    return render(request, 'html/editar_material.html', {'form': form, 'material': material})

@login_required
def cambiar_estado_material(request, pk):
    if request.method == 'POST':
        material = get_object_or_404(Material, pk=pk, autor=request.user)
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Material.ESTADO_CHOICES):
            material.estado = nuevo_estado
            material.save()
            messages.success(request, 'Estado de Material actualizado exitosamente')
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def eliminar_material(request, pk):
    material = get_object_or_404(Material, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        material.estado = 'eliminado'
        material.save()
        messages.success(request, 'Material eliminado exitosamente')
        return redirect('mis_materiales')
    
    return render(request, 'html/confirmar_eliminar_material.html', {
        'material': material
    })

#CARRITO---------------------------------------------------------
@login_required
def agregar_al_carrito(request, material_id):
    material = get_object_or_404(Material, id=material_id, estado='publicado')
    
    # Verificar que no sea un material propio
    if material.autor == request.user:
        return JsonResponse({
            'success': False,
            'message': 'No puedes agregar tus propios materiales al carrito'
        })
    
    # Crear o verificar si ya existe
    item, created = CarritoItem.objects.get_or_create(
        usuario=request.user,
        material=material
    )
    
    if created:
        return JsonResponse({
            'success': True,
            'message': 'Material agregado al carrito',
            'itemCount': CarritoItem.objects.filter(usuario=request.user).count()
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'El material ya está en tu carrito'
        })

@login_required
def obtener_carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)[:3]
    data = [{
        'id': item.material.id,
        'titulo': item.material.titulo,
        'precio': str(item.material.precio),
        'imagen': item.material.imagen.url if item.material.imagen else None
    } for item in items]
    
    return JsonResponse({
        'items': data,
        'itemCount': CarritoItem.objects.filter(usuario=request.user).count()
    })

@login_required
def eliminar_del_carrito(request, material_id):
    CarritoItem.objects.filter(
        usuario=request.user,
        material_id=material_id
    ).delete()
    
    return JsonResponse({
        'success': True,
        'itemCount': CarritoItem.objects.filter(usuario=request.user).count()
    })

@login_required
def vista_compra(request):
    items_carrito = CarritoItem.objects.filter(usuario=request.user)
    if not items_carrito:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('lista_materiales')
    
    total = sum(item.material.precio for item in items_carrito)
    vendedores = []
    
    # Obtener información de pago de los vendedores
    for item in items_carrito:
        vendedor = {
            'usuario': item.material.autor,
            'perfil': item.material.autor.perfilusuario,
            'materiales': [],
            'subtotal': 0
        }
        for carrito_item in items_carrito:
            if carrito_item.material.autor == item.material.autor:
                vendedor['materiales'].append(carrito_item.material)
                vendedor['subtotal'] += carrito_item.material.precio
        
        if vendedor not in vendedores:
            vendedores.append(vendedor)
    
    return render(request, 'html/compra.html', {
        'items': items_carrito,
        'total': total,
        'vendedores': vendedores
    })

@login_required
def procesar_compra(request):
    if request.method == 'POST':
        items_carrito = CarritoItem.objects.filter(usuario=request.user)
        if not items_carrito:
            messages.error(request, 'No hay items en el carrito')
            return redirect('lista_materiales')

        # Crear la compra
        compra = Compra.objects.create(
            usuario=request.user,
            total=sum(item.material.precio for item in items_carrito),
            codigo_seguimiento=str(uuid.uuid4().hex[:8].upper())
        )

        # Crear detalles de compra y notificaciones para vendedores
        vendedores_notificados = set()  # Para evitar notificaciones duplicadas
        
        for item in items_carrito:
            DetalleCompra.objects.create(
                compra=compra,
                material=item.material,
                precio_unitario=item.material.precio
            )
            
            # Crear notificación para el vendedor si aún no ha sido notificado
            if item.material.autor.id not in vendedores_notificados:
                Notificacion.objects.create(
                    usuario=item.material.autor,
                    tipo='pago_recibido',
                    titulo='Nuevo pago por verificar',
                    mensaje=f'El usuario {request.user.username} ha realizado una compra y subido un comprobante de pago. Por favor, verifica el pago.',
                    referencia_id=compra.id,
                    referencia_tipo='compra'
                )
                vendedores_notificados.add(item.material.autor.id)

        # Procesar comprobante si existe
        if 'comprobante' in request.FILES:
            compra.comprobante = request.FILES['comprobante']
            compra.estado = 'pagado'
            compra.fecha_pago = timezone.now()
            compra.save()

            # Notificar al comprador
            Notificacion.objects.create(
                usuario=request.user,
                tipo='compra_realizada',
                titulo='Compra realizada con éxito',
                mensaje=f'Tu compra #{compra.codigo_seguimiento} ha sido registrada y está en espera de confirmación.',
                referencia_id=compra.id,
                referencia_tipo='compra'
            )

        # Limpiar carrito
        items_carrito.delete()

        messages.success(request, 
            f'¡Compra realizada con éxito! Tu código de seguimiento es: {compra.codigo_seguimiento}')
        return redirect('mis_compras')

    return redirect('vista_compra')

@login_required
def cancelar_compra(request):
    if request.method == 'POST':
        items_carrito = CarritoItem.objects.filter(usuario=request.user)
        items_carrito.delete()
        messages.info(request, 'Has cancelado tu compra')
    return redirect('lista_materiales')

# NOTIFICACIONES
@login_required
def notificaciones_recientes(request):
    notificaciones = Notificacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha_creacion')[:5]
    
    data = [{
        'id': notif.id,
        'titulo': notif.titulo,
        'mensaje': notif.mensaje,
        'tipo': notif.tipo,
        'leida': notif.leida,
        'fecha_relativa': timesince(notif.fecha_creacion),
        'referencia_id': notif.referencia_id,
        'imagen': notif.get_imagen_url() if hasattr(notif, 'get_imagen_url') else None
    } for notif in notificaciones]
    
    return JsonResponse({
        'notificaciones': data,
        'no_leidas': Notificacion.objects.filter(usuario=request.user, leida=False).count()
    })

@login_required
@require_POST
def marcar_notificaciones_leidas(request):
    Notificacion.objects.filter(usuario=request.user).update(leida=True)
    return JsonResponse({'success': True})

@login_required
def todas_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    return render(request, 'html/notificaciones.html', {
        'notificaciones': notificaciones
    })

@login_required
def verificar_pago(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    if not compra.materiales.filter(autor=request.user).exists():
        messages.error(request, 'No tienes permiso para verificar este pago')
        return redirect('inicio')
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'confirmar':
            compra.estado = 'confirmado'
            compra.fecha_confirmacion = timezone.now()
            # Marcar materiales como vendidos
            compra.materiales.filter(autor=request.user).update(estado='vendido')
            
            # Notificar al comprador
            Notificacion.objects.create(
                usuario=compra.usuario,
                tipo='pago_confirmado',
                titulo='Pago confirmado',
                mensaje=f'Tu pago por la compra #{compra.codigo_seguimiento} ha sido confirmado.',
                referencia_id=compra.id,
                referencia_tipo='compra'
            )

        elif accion == 'rechazar':
            compra.estado = 'rechazado'
            compra.motivo_rechazo = request.POST.get('motivo_rechazo')
            
            # Notificar al comprador
            Notificacion.objects.create(
                usuario=compra.usuario,
                tipo='pago_rechazado',
                titulo='Pago rechazado',
                mensaje=f'Tu pago por la compra #{compra.codigo_seguimiento} ha sido rechazado. Motivo: {compra.motivo_rechazo}',
                referencia_id=compra.id,
                referencia_tipo='compra'
            )
        
        compra.save()
        messages.success(request, f'Has {accion}ado el pago correctamente')
        return redirect('todas_notificaciones')
    
    return render(request, 'html/verificar_pago.html', {
        'compra': compra
    })

@login_required
def mis_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'html/mis_compras.html', {
        'compras': compras
    })

@login_required
def mis_ventas(request):
    # Obtener todas las ventas (materiales vendidos)
    ventas = DetalleCompra.objects.filter(
        material__autor=request.user
    ).select_related('compra', 'material')

    # Estadísticas generales
    estadisticas = {
        'total_ventas': ventas.count(),
        'ingresos_totales': ventas.aggregate(total=Sum('precio_unitario'))['total'] or 0,
        'ventas_mes_actual': ventas.filter(
            compra__fecha_confirmacion__month=timezone.now().month
        ).count(),
        'ingresos_mes': ventas.filter(
            compra__fecha_confirmacion__month=timezone.now().month
        ).aggregate(total=Sum('precio_unitario'))['total'] or 0,
    }

    # Ventas por mes
    ventas_por_mes = ventas.annotate(
        mes=TruncMonth('compra__fecha_confirmacion')
    ).values('mes').annotate(
        total=Sum('precio_unitario'),
        cantidad=Count('id')
    ).order_by('-mes')

    # Materiales más vendidos
    materiales_populares = Material.objects.filter(
        autor=request.user,
        estado='vendido'
    ).annotate(
        total_ventas=Count('detallecompra')
    ).order_by('-total_ventas')[:5]

    return render(request, 'html/mis_ventas.html', {
        'ventas': ventas,
        'estadisticas': estadisticas,
        'ventas_por_mes': ventas_por_mes,
        'materiales_populares': materiales_populares
    })

@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(DetalleCompra, 
                             id=venta_id, 
                             material__autor=request.user)
    
    # Obtener historial de ventas del mismo material
    historial_material = DetalleCompra.objects.filter(
        material=venta.material
    ).exclude(
        id=venta_id
    ).select_related('compra').order_by('-compra__fecha_confirmacion')[:5]
    
    # Obtener historial de compras del usuario
    historial_comprador = DetalleCompra.objects.filter(
        compra__usuario=venta.compra.usuario,
        material__autor=request.user
    ).exclude(
        id=venta_id
    ).select_related('material', 'compra').order_by('-compra__fecha_confirmacion')
    
    return render(request, 'html/detalle_venta.html', {
        'venta': venta,
        'historial_material': historial_material,
        'historial_comprador': historial_comprador,
    })