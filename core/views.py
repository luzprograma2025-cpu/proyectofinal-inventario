# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required  
from django.contrib import messages
from .models import Material 
from django.db.models import Q 

def index(request):
    if request.user.is_authenticated:
        return redirect('almacen')

    if request.method == 'POST':
        usuario = request.POST.get('username')
        contrasena = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=contrasena)
        
        if user is not None:
            login(request, user)
            return redirect('almacen')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'core/index.html')

@login_required
def almacen(request):
    return render(request, 'core/almacen.html')

def exit(request):
    logout(request)
    return redirect('index')

@login_required
def lista_materiales(request, tipo_material):
    materiales = Material.objects.filter(tipo=tipo_material)
    
    if tipo_material == 'critico':
        titulo = "Material Crítico"
    else:
        titulo = "Material Interno"
        
    context = {
        'materiales': materiales,
        'titulo': titulo
    }
    return render(request, 'core/lista_materiales.html', context)

@login_required
def actualizar_cantidad(request, material_id):
    # 1. La protección de Staff 
    if not request.user.is_staff:
        return redirect('almacen')

    # 2. Buscamos el material 
    material = Material.objects.get(id=material_id)

    # 3. ESTA ES LA LÓGICA QUE CAMBIA
    if request.method == 'POST':
       
        nueva_cantidad = request.POST.get('cantidad_nueva')
        
        
        if nueva_cantidad is not None and nueva_cantidad.isdigit():
            material.cantidad = int(nueva_cantidad)
            
            
            if material.cantidad < 0:
                material.cantidad = 0
                
            material.save() 

    # 4. Redirigimos al usuario a la misma página
    return redirect('lista_materiales', tipo_material=material.tipo)

# 
# ESTA ES LA FUNCIÓN DE BÚSQUEDA 
#
@login_required
def search(request):
   
    query = request.GET.get('q')
    
    if query:
       
        materiales = Material.objects.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query)
        )
        titulo = f"Resultados para: '{query}'"
    else:
    
        materiales = []
        titulo = "Por favor ingresa un término de búsqueda"

    context = {
        'materiales': materiales,
        'titulo': titulo
    }
    
    return render(request, 'core/lista_materiales.html', context)