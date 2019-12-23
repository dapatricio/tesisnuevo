from django import forms
from .models import Usuario, RtaUsr

class UsuarioForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ['nombUsuario', 'cedula', 'correo', 'clave', 'id_tipoUsr', 'id_dependencia']

class ContactoForm(forms.Form):
	correo=forms.EmailField()
	mensaje=forms.CharField()