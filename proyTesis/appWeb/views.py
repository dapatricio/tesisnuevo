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
import pandas as pd
# Local Apps
from .forms import ContactoForm, ProfileForm, UserForm, UserLoginForm, UserUpdateForm
from .models import *

#Imports para la grafica
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
import json

from django.http import HttpResponse
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

def dependency(request, id_tipodep):
    dependency = Dependencia.objects.filter(id_tipoDep=id_tipodep).values("id_dependencia", "nombDependencia")
    return JsonResponse({'dependency':list(dependency)})

#Excel
import xlwt

from django.http import HttpResponse
from django.contrib.auth.models import *

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="base tesis.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws1 = wb.add_sheet('Respuestas cuestionario',cell_overwrite_ok=True)
    ws2 = wb.add_sheet('Respuestas generales',cell_overwrite_ok=True)

    # Sheet header, first row
    row_num = 0
    row_num1 = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columnsws1 = ['Usuario', 'Tipo Usuario','Genero', 'Dependencia', 'Valor Rta']
    columnsws2 = ['Usuario', 'Respuesta']

    #Hoja Preguntas cuestionario Especifico
    
    for col_num in range(len(columnsws1)):
        ws1.write(row_num, col_num, columnsws1[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows1 = RtaUsr.objects.values('id_usr__username', 'id_usr__userprofile__id_tipoUsr__tipo_usuario', 'id_usr__userprofile__genero', 'id_pregunta__id_competencia__nombCompetencia', 'id_usr__userprofile__id_dependencia__nombDependencia', 'rtaUser').order_by('id_pregunta__id_competencia__nombCompetencia')
    df = pd.DataFrame(rows1)
    df = df.groupby("id_usr__username").agg(lambda x: list(x))
    row = 1
    col = 0
    for item in df.iterrows():
        username = item[0]
        ws1.write(row, col, username, font_style)
        tipo_usuario = item[1][0][0]
        col +=1
        ws1.write(row, col, tipo_usuario, font_style)
        genero = item[1][1][0]
        col +=1
        ws1.write(row, col, genero, font_style)
        dependencia = item[1][3][0]
        col +=1
        ws1.write(row, col, dependencia, font_style)
        col += 1
        for rta, tit in zip(item[1]['rtaUser'], item[1][2]):
            ws1.write(0, col, "Comp. " + str(tit), font_style)
            ws1.write(row, col, rta, font_style)
            col += 1
        row += 1
        col = 0

    #Hoja Preguntas cuestionario General
    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    for col_num1 in range(len(columnsws2)):
        ws2.write(row_num, col_num1, columnsws1[col_num1], font_style)

    font_style = xlwt.XFStyle()
    rows2 = RtaUsrGeneral.objects.values('id_usr__username', 'id_pregunta__pregunta', 'rta_user').order_by('id_pregunta__pregunta')
    df = pd.DataFrame(rows2)
    df = df.groupby("id_usr__username").agg(lambda x: list(x))
    row = 1
    col = 0
    for item1 in df.iterrows():
        username = item1[0]
        ws2.write(row, col, username, font_style)
        col += 1
        for rta1, tit2 in zip(item1[1]['rta_user'], item1[1][0]):
            ws2.write(0, col, "Preg. " + str(tit2), font_style)
            ws2.write(row, col, rta1, font_style)
            col += 1
        row += 1
        col = 0    

    wb.save(response)
    return response    
