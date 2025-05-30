from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Material, PerfilUsuario  # Quitamos Facultad
from django.db.models import Q
from .forms import MaterialForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.autor = request.user
            material.save()
            messages.success(request, '¡Material publicado exitosamente...!' +  material.titulo)
            return redirect('lista_materiales')
    else:
        form = MaterialForm()
    
    return render(request, 'html/publicar_material.html', {'form': form})

def lista_materiales(request):
    materiales = Material.objects.all()
    
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
        perfil.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
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
        
        perfil.save()
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('perfil_usuario')

    context = {
        'perfil': perfil,
        'redes_sociales': json.dumps(perfil.redes_sociales)
    }
    return render(request, 'html/perfil_usuario.html', context)

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