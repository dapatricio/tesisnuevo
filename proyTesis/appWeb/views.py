# Python
import datetime
import pytz
from datetime import datetime

# Django core
from django.contrib.auth import (
    authenticate,
    authenticate,
    get_user_model,
    login,
    login,
    logout,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.http import (
    Http404,
    HttpResponse,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    redirect,
    render,
    render,
    render,
    render_to_response,
)
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# Local Apps
from .forms import ContactoForm, ProfileForm, UserForm, UserLoginForm, UserUpdateForm
from .models import *

#Imports para la grafica
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt

# Create your views here.
def index(request):
    return render(request, "index.html")


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


class Informacion(ListView):
    model = Area_Competencia
    template_name = "informacion.html"

def graphica(request):

    labels = ['C1', 'C2', 'C3', 'C4', 'C5']
    men_means = [20, 34, 30, 35, 27]
    women_means = [25, 32, 34, 20, 25]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, men_means, width, label='Nivel Obtenidoooo')
    rects2 = ax.bar(x + width/2, women_means, width, label='Nivel Recomendadooooo')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Nivel')
    ax.set_title('Resultado vs Recomendado')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    #plt.show()
    plt.savefig('../static/graphimages/saved_figure.png')

    return render(request, 'pdf.html',{'graphica':graphica})