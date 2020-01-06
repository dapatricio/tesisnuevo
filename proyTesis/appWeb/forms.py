from django import forms
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import RtaUsr, Profile

# class UsuarioForm(forms.ModelForm):
# 	class Meta:
# 		model = Usuario
# 		fields = (
# 		'nombUsuario', 
# 		'cedula', 
# 		'correo', 
# 		'clave', 
# 		'id_tipoUsr', 
# 		'id_dependencia',
# 		)
# 		widgets = {
#             'nombUsuario':forms.TextInput(attrs={'placeholder': ' Nombres y Apellidos aqui...'}), 
# 			'cedula':forms.TextInput(attrs={'placeholder': ' 1101010101'}), 
# 			'correo':forms.TextInput(attrs={'placeholder': ' ejemplo@gmail.com'}), 
# 			'clave':forms.TextInput(attrs={'placeholder': ' Escriba su clave aqui...'}), 
#         }

class ContactoForm(forms.Form):
	nombre=forms.CharField(label='Nombre y Apellido:', widget=forms.TextInput(attrs={'placeholder': ' Nombres y Apellidos aqui...'}))
	asunto=forms.CharField(label='Asunto o duda:', widget=forms.TextInput(attrs={'placeholder': ' Asunto del mensaje aqui...'}))
	correo=forms.EmailField(label='Correo electrónico:', widget=forms.TextInput(attrs={'placeholder': ' Escriba su correo electronico aqui...'}))
	mensaje=forms.CharField(label='Mensaje a enviar: ', widget=forms.Textarea(attrs={'placeholder': ' Escriba su mensaje a enviar aqui...'}))

class UserForm(forms.ModelForm):
	username=forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'placeholder': ' Escriba su nombre de usuario...'}))
	first_name=forms.CharField(label='Nombres de la persona', widget=forms.TextInput(attrs={'placeholder': ' Escriba sus nombres...'}))
	last_name=forms.CharField(label='Apellidos de la persona', widget=forms.TextInput(attrs={'placeholder': ' Escriba sus apellidos...'}))
	email=forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': ' ejemplo@gmail.com'}))
	password=forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': ' Escriba su clave aqui...'}))

	class Meta:
		model = User
		fields = (
			'username', 
			'first_name', 
			'last_name', 
			'email', 
			'password',
		)

class ProfileForm(forms.ModelForm):
	cedula=forms.CharField(label='Cédula', widget=forms.TextInput(attrs={'placeholder': ' 1101010101'}))

	class Meta:
		model = Profile
		fields = (
			'cedula',
			'id_tipoUsr', 
			'id_dependencia',
			)