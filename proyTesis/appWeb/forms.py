from django import forms
from .models import Usuario, RtaUsr

class UsuarioForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = (
		'nombUsuario', 
		'cedula', 
		'correo', 
		'clave', 
		'id_tipoUsr', 
		'id_dependencia',
		)
		widgets = {
            'nombUsuario':forms.TextInput(attrs={'placeholder': ' Nombres y Apellidos aqui...'}), 
			'cedula':forms.TextInput(attrs={'placeholder': ' 1101010101'}), 
			'correo':forms.TextInput(attrs={'placeholder': ' ejemplo@gmail.com'}), 
			'clave':forms.TextInput(attrs={'placeholder': ' Escriba su clave aqui...'}), 
        }

class ContactoForm(forms.Form):
	nombre=forms.CharField(label='Nombre y Apellido:', widget=forms.TextInput(attrs={'placeholder': ' Nombres y Apellidos aqui...'}))
	asunto=forms.CharField(label='Asunto o duda:', widget=forms.TextInput(attrs={'placeholder': ' Asunto del mensaje aqui...'}))
	correo=forms.EmailField(label='Correo electrónico:', widget=forms.TextInput(attrs={'placeholder': ' Escriba su correo electronico aqui...'}))
	mensaje=forms.CharField(label='Mensaje a enviar: ', widget=forms.Textarea(attrs={'placeholder': ' Escriba su mensaje a enviar aqui...'}))