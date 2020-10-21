from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, Transporte
from django.forms import ModelForm


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormularioUsuario(forms.ModelForm):
    """ Formulario de Registro de un Usuario en la base de datos
    Variables:
        - password1:    Contraseña
        - password2:    Verificación de la contraseña
    """
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label='Contraseña de Confirmación', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = Usuario
        fields = ('__all__')

    def clean_password2(self):
        """ Validación de Contraseña
        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.
        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido',
                  'direccion', 'telefono', 'email', 'username','password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': "Ingrese su contraseña."}),
            'username': forms.TextInput(attrs={'placeholder': "Ingrese su nombre de usuario a utilizar"}),
        }
        labels = {
            'username': ("Nombre de usuario:")
        }

class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transporte
        fields = ('__all__')
        exclude = ['id_transporte','id_cliente']
        labels = {
        'tamanio': ("Tamaño de su transporte:"),
        'capacidad_carga':("Capacidad de carga en KG.")
        }


