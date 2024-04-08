from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambiar la etiqueta del campo 'username' a 'Usuario'
        self.fields['username'].label = _('Usuario')
        # Cambiar la etiqueta del campo 'password1' a 'Contraseña'
        self.fields['password1'].label = _('Contraseña')
        # Cambiar la etiqueta del campo 'password2' a 'Confirmar contraseña'
        self.fields['password2'].label = _('Confirmar contraseña')


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambiar la etiqueta del campo 'username' a 'Usuario'
        self.fields['username'].label = _('Usuario')
        # Cambiar la etiqueta del campo 'password' a 'Contraseña'
        self.fields['password'].label = _('Contraseña')


class CustomUserChangeForm(UserChangeForm):
    # Añadir campos personalizados para 'password' y 'confirm_password'
    password = forms.CharField(label=_("Contraseña"), strip=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label=_("Confirmar contraseña"), strip=False, widget=forms.PasswordInput)

    class Meta(UserChangeForm.Meta):
        # Mostrar solo los campos 'username' y 'password'
        fields = ['username', 'password']
        help_texts = {
            'username': None,  # Eliminar el texto de ayuda para el campo de 'username'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer el campo de 'username' como de solo lectura
        self.fields['username'].widget.attrs['readonly'] = True
