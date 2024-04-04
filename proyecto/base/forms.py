from django import forms
from django.contrib.auth.forms import UserChangeForm


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput)

    class Meta(UserChangeForm.Meta):
        fields = ['username', 'password']
        help_texts = {
            'username': None,  # Esto quita el texto de ayuda del campo de nombre de usuario
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True  # Establecer el campo de nombre de usuario como de solo lectura
