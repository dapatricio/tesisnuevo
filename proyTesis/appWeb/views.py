from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import ContactoForm, UserForm, ProfileForm, UserLoginForm, UserUpdateForm
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.shortcuts import render
from django.shortcuts import render, redirect

# from .forms import *
from .models import *
from datetime import datetime
from django.http import JsonResponse
import pytz, datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView


# Create your views here.
def index(request):
    return render(request, "index.html")


def informacion(request):
    return render(request, "informacion.html")


def proposito(request):
    return render(request, "proposito.html")


def contacto(request):
    if request.method == "POST":
        contacto_form = ContactoForm(request.POST)
        if contacto_form.is_valid():
            asunto = contacto_form.cleaned_data["asunto"]
            mensaje = (
                "El mensaje indica:\n"
                + contacto_form.cleaned_data["mensaje"]
                + "\n\n Enviado por: "
                + contacto_form.cleaned_data["nombre"]
                + "\n Correo electrónico: "
                + contacto_form.cleaned_data["correo"]
            )
            mail = EmailMessage(asunto, mensaje, to=["dppenarreta@gmail.com"])
            mail.send()
        return HttpResponseRedirect("/")
    else:
        contacto_form = ContactoForm()

    return render(request, "contacto.html", {"contacto_form": contacto_form})


# def login(request):
#     return render(request, "login.html")


def registro(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            usuario = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = usuario
            profile.save()
            return redirect("login")
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(
        request, "registro.html", {"user_form": user_form, "profile_form": profile_form}
    )


class UpdateUserView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "cuestionario/user.html"
    success_url = "/login/cuestionario/"
