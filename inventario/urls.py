# inventario/urls.py
from django.contrib import admin
from django.urls import path
from core import views # Importamos las vistas de 'core'

# Para servir archivos de media (fotos) en modo DEBUG
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs de Core (Nuestra app)
    path('', views.index, name='index'),
    path('almacen/', views.almacen, name='almacen'),
    path('logout/', views.exit, name='logout'),
    
    # URL para la lista de materiales (Crítico o Interno)
    path('materiales/<str:tipo_material>/', views.lista_materiales, name='lista_materiales'),
    
    # URL para actualizar la cantidad (botones + y -)
    path('actualizar/<int:material_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    
    # ¡NUEVA URL PARA LA BÚSQUEDA!
    path('search/', views.search, name='search'),

    # URL del Admin de Django
    path('admin/', admin.site.urls),
]

# Añadimos la configuración para servir las fotos que subimos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)