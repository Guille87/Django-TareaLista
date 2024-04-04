from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView

from .forms import CustomUserChangeForm
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


class EditarPerfil(UpdateView):
    """
    Vista que permite a los usuarios editar su perfil.
    """
    model = User
    form_class = CustomUserChangeForm  # Usa el formulario personalizado
    template_name = 'editar_perfil.html'
    success_url = reverse_lazy('tareas')

    def get_object(self, queryset=None):
        """
        Retorna el objeto que se está actualizando.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Método llamado si el formulario es válido.
        """
        user = form.save(commit=False)  # No guarda el usuario todavía para poder hacer validaciones adicionales

        # Obtiene la contraseña actual proporcionada en el formulario
        entered_password = form.cleaned_data.get('password')

        # Comprueba si la contraseña actual proporcionada coincide con la contraseña actual del usuario
        if not authenticate(username=user.username, password=entered_password):
            # Si las contraseñas no coinciden, agrega un error al formulario
            form.add_error('password', 'La contraseña actual no es válida.')
            return self.form_invalid(form)

        # Cambiar la contraseña si se proporcionó una nueva
        nueva_contrasenia = self.request.POST.get('new_password')
        confirm_password = self.request.POST.get('confirm_password')
        if nueva_contrasenia != confirm_password:
            form.add_error('confirm_password', 'Las contraseñas no coinciden.')
            return self.form_invalid(form)

        if nueva_contrasenia:
            user.set_password(nueva_contrasenia)
            user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Método llamado si el formulario es inválido.
        """
        print("El formulario es inválido. Errores:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class ListaPendientes(LoginRequiredMixin, ListView):
    """
    Vista que muestra la lista de tareas pendientes del usuario actual.
    Filtra las tareas por el usuario actual y proporciona funcionalidad de búsqueda.
    """
    model = Tarea
    context_object_name = 'tareas'
    paginate_by = 10  # Número de tareas por página

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.incompletas_count = 0

    def get_queryset(self):
        """
        Retorna el queryset de tareas filtrado por el usuario actual.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(usuario=self.request.user)
        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            queryset = queryset.filter(titulo__icontains=valor_buscado)

        # Contar las tareas incompletas y almacenar el conteo como una variable de clase
        self.incompletas_count = queryset.filter(completo=False).count()
        return queryset

    def get_context_data(self, **kwargs):
        """
        Agrega información adicional al contexto de la vista, como el número total de tareas pendientes y el valor de búsqueda.
        """
        context = super().get_context_data(**kwargs)
        # Utiliza la variable de clase para obtener el conteo de tareas incompletas
        context['count'] = self.incompletas_count
        context['valor_buscado'] = self.request.GET.get('area-buscar') or ''
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

    def form_valid(self, form):
        tarea = form.save(commit=False)
        if tarea.completo:
            tarea.completado = timezone.now()  # Establecer la fecha y hora de completado
        tarea.save()
        return super().form_valid(form)


class EliminarTarea(LoginRequiredMixin, DeleteView):
    """
    Vista que permite a los usuarios eliminar una tarea existente.
    """
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')
