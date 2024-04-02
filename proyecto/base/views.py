from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarea


class Logueo(LoginView):
    """
    Vista que maneja el inicio de sesión de los usuarios.
    Utiliza la plantilla 'base/login.html' para mostrar el formulario de inicio de sesión.
    Redirige a la página de tareas ('tareas') si el usuario ya está autenticado.
    """
    template_name = "base/login.html"
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Retorna la URL de redirección después de que el usuario inicie sesión correctamente.
        """
        return reverse_lazy('tareas')


class PaginaRegistro(FormView):
    """
    Vista que maneja el registro de nuevos usuarios.
    Utiliza la plantilla 'base/registro.html' para mostrar el formulario de registro.
    Redirige a la página de tareas ('tareas') después de un registro exitoso.
    """
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        """
        Guarda el nuevo usuario y lo inicia sesión automáticamente después del registro.
        """
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        """
        Redirige a los usuarios autenticados a la página de tareas ('tareas').
        """
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(PaginaRegistro, self).get(*args, **kwargs)


class ListaPendientes(LoginRequiredMixin, ListView):
    """
    Vista que muestra la lista de tareas pendientes del usuario actual.
    Filtra las tareas por el usuario actual y proporciona funcionalidad de búsqueda.
    """
    model = Tarea
    context_object_name = 'tareas'

    def get_context_data(self, **kwargs):
        """
        Agrega información adicional al contexto de la vista, como el número total de tareas pendientes y el valor de búsqueda.
        """
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()

        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)
        context['valor_buscado'] = valor_buscado
        return context


class DetalleTarea(LoginRequiredMixin, DetailView):
    """
    Vista que muestra los detalles de una tarea específica.
    Utiliza la plantilla 'base/tarea.html' para renderizar los detalles.
    """
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


class CrearTarea(LoginRequiredMixin, CreateView):
    """
    Vista que permite a los usuarios crear una nueva tarea.
    Utiliza un formulario con campos 'titulo', 'descripcion' y 'completo'.
    Asigna automáticamente la tarea al usuario actual.
    """
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        """
        Guarda la tarea y asigna al usuario actual como el propietario de la tarea.
        """
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)


class EditarTarea(LoginRequiredMixin, UpdateView):
    """
    Vista que permite a los usuarios editar una tarea existente.
    Utiliza un formulario con campos 'titulo', 'descripcion' y 'completo'.
    """
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo']
    success_url = reverse_lazy('tareas')


class EliminarTarea(LoginRequiredMixin, DeleteView):
    """
    Vista que permite a los usuarios eliminar una tarea existente.
    """
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')
