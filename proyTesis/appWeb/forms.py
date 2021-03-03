from django import forms
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import RtaUsr, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre y Apellido:",
        widget=forms.TextInput(attrs={"placeholder": " Nombres y Apellidos aqui..."}),
    )
    asunto = forms.CharField(
        label="Asunto o duda:",
        widget=forms.TextInput(attrs={"placeholder": " Asunto del mensaje aqui..."}),
    )
    correo = forms.EmailField(
        label="Correo electrónico:",
        widget=forms.TextInput(
            attrs={"placeholder": " Escriba su correo electronico aqui..."}
        ),
    )
    mensaje = forms.CharField(
        label="Mensaje a enviar: ",
        widget=forms.Textarea(
            attrs={"placeholder": " Escriba su mensaje a enviar aqui..."}
        ),
    )


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nombres")
    last_name = forms.CharField(max_length=30, required=True, label="Apellidos")
    email = forms.EmailField(
        max_length=254,
        help_text="Necesario. Ingresar una dirección de correo electrónico válida.",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class ProfileForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = (
            "genero",
            "id_tipoUsr",
            "id_dependencia",
        )


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise form.ValidationError("El usuario no existe")
            if not user.check_password(password):
                raise form.ValidationError("La contraseña es incorrecta")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
