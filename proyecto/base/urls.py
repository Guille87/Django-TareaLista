from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views
from .views import ListaPendientes, DetalleTarea, CrearTarea, EditarTarea, EliminarTarea, Logueo, PaginaRegistro, EditarPerfil

urlpatterns = [
    path('', ListaPendientes.as_view(), name='tareas'),
    path('login/', Logueo.as_view(), name='login'),
    path('registro/', PaginaRegistro.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('tarea/<int:pk>', DetalleTarea.as_view(), name='tarea'),
    path('editar-perfil/<int:pk>/', EditarPerfil.as_view(), name='editar-perfil'),
    path('crear-tarea/', CrearTarea.as_view(), name='crear-tarea'),
    path('editar-tarea/<int:pk>', EditarTarea.as_view(), name='editar-tarea'),
    path('eliminar-tarea/<int:pk>', EliminarTarea.as_view(), name='eliminar-tarea'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('tarea_list/', views.cambiar_idioma, name='cambiar_idioma'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
