from django import forms
from django.db import IntegrityError
from django.contrib.auth.models import User
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
        help_text="Necesario. Informar una dirección de correo electrónico válida.",
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
        widgets = {
            "id_ficha_predial": forms.HiddenInput(),
            "clave_catastral": forms.HiddenInput(),
            "descripcion": forms.Textarea(attrs={"rows": 4}),
        }


class ProfileForm(forms.ModelForm):
    cedula = forms.CharField(
        label="Cédula", widget=forms.TextInput(attrs={"placeholder": " 1101010101"})
    )

    class Meta:
        model = Profile
        fields = (
            "cedula",
            "id_tipoUsr",
            "id_dependencia",
        )
