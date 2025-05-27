from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required #Login requerido
from .models import Material
from django.db.models import Q
from .forms import MaterialForm

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
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'html/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

#MOSTRAR MATERIALES---------------------------------------------------------
# filepath: c:\Users\GUILDER\Desktop\PROYECTOS\ProyectosDjango\mercadoestudios\DameDoy\views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material
from .forms import MaterialForm

@login_required
def publicar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.autor = request.user
            material.save()
            messages.success(request, '¡Material publicado exitosamente!')
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
    
    # Ordenamiento
    orden = request.GET.get('orden', '-fecha_publicacion')
    materiales = materiales.order_by(orden)
    
    # Obtener valores únicos para los filtros
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