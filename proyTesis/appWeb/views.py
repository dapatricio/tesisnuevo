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
    ws1 = wb.add_sheet('Respuestas Usuarios')
    ws2 = wb.add_sheet('Perfiles', cell_overwrite_ok=True)
    ws3 = wb.add_sheet('Usuarios', cell_overwrite_ok=True)
    ws4 = wb.add_sheet('Tipos', cell_overwrite_ok=True)
    ws5 = wb.add_sheet('Preguntas', cell_overwrite_ok=True)
    ws6 = wb.add_sheet('UTPL', cell_overwrite_ok=True)
    ws7 = wb.add_sheet('Detalle DigComp', cell_overwrite_ok=True)
    ws8 = wb.add_sheet('Nivel Recomendado', cell_overwrite_ok=True)
    ws9 = wb.add_sheet('Respuestas Generales', cell_overwrite_ok=True)


    # Sheet header, first row
    row_num = 0
    row_num1 = 0
    row_num2 = 0
    row_num3 = 0
    row_num4 = 0
    row_num5 = 0
    row_num6 = 0
    row_num7 = 0
    row_num8 = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columnsws1 = ['Id Usuario', 'Id Pregunta', 'Valor Rta']
    columnsws2 = ['Id Usuario', 'Id Tipo Usuario', 'Id Dependencia', 'Genero']
    columnsws3 = ['Id Usuario', 'Nombres', 'Apellidos', 'Usuario']
    columnsws4 = ['Id tipo Usuario', 'Descripción']
    columnsws5 = ['Id pregunta', 'Pregunta', 'Id competencia', 'Id tipo cuestionario']
    columnsws6 = ['Id tipo Cuestionario', 'Descripción', 'id tipo Usuario']
    columnsws7 = ['Id tipo Usuario', 'Descripción']
    columnsws8 = ['Id deoendencia', 'Dependencia', 'Id area', 'id tipo dependencia']
    columnsws9 = ['Id facultad', 'Facultad']
    columnsws10 = ['Id competencia', 'Detalle', 'Id area']
    columnsws11 = ['Id area', "Detalle"]
    columnsws12 = ['Id nivel', "Nivel", 'Id competencia', 'Id dependencia']
    columnsws13 = ['Id respuesta', "Respuesta", 'Valor', 'Pregunta']

    #Hoja Respuestas
    
    for col_num in range(len(columnsws1)):
        ws1.write(row_num, col_num, columnsws1[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows1 = RtaUsr.objects.all().values_list('id_usr', 'id_pregunta', 'rtaUser')

    for row in rows1:
        row_num += 1
        for col_num in range(len(row)):
            ws1.write(row_num, col_num, row[col_num], font_style)

    #Hoja Perfiles
    columnsws2 = ['Id Usuario', 'Id Tipo Usuario', 'Id Dependencia', 'Genero']
    for col_num1 in range(len(columnsws2)):
        ws2.write(row_num1, col_num1, columnsws2[col_num1], font_style)

    font_style = xlwt.XFStyle()
    rows2 = Profile.objects.all().values_list('user', 'id_tipoUsr', 'id_dependencia', 'genero')
    
    for row1 in rows2:
        row_num1 += 1
        for col_num1 in range(len(row1)):
            ws2.write(row_num1, col_num1, row1[col_num1], font_style)

    #Hoja Usuarios
    
    for col_num2 in range(len(columnsws3)):
        ws3.write(row_num2, col_num2, columnsws3[col_num2], font_style)        

    font_style = xlwt.XFStyle()
    rows3 = User.objects.all().values_list('id','first_name', 'last_name', 'username')

    for row1 in rows3:
        row_num2 += 1
        for col_num2 in range(len(row1)):
            ws3.write(row_num2, col_num2, row1[col_num2], font_style)                   


    #Hoja Tipo Usuarios / Cuestionarios / Dependencias
        #Tipo usuarios
    for col_num3 in range(len(columnsws4)):
        ws4.write(row_num3, col_num3, columnsws4[col_num3], font_style)        

    font_style = xlwt.XFStyle()
    rows4 = TipoUsr.objects.all().values_list('id_tipoUsr','tipo_usuario')

    for row1 in rows4:
        row_num3 += 1
        for col_num3 in range(len(row1)):
            ws4.write(row_num3, col_num3, row1[col_num3], font_style)

        #Cuestionarios
    for col_num4 in range(len(columnsws6)):
        ws4.write(row_num3, col_num4, columnsws6[col_num4], font_style)        

    font_style = xlwt.XFStyle()
    rows5 = TipoCuest.objects.all().values_list('id_tipoCuest','nombCuest', 'id_tipoUsr')

    for row1 in rows5:
        row_num3 += 1
        for col_num4 in range(len(row1)):
            ws4.write(row_num3, col_num4, row1[col_num4], font_style)

        #Dependencias
    for col_num5 in range(len(columnsws7)):
        ws4.write(row_num3, col_num5, columnsws7[col_num5], font_style)        

    font_style = xlwt.XFStyle()
    rows6 = TipoDep.objects.all().values_list('id_tipoDep','tipo_dep')

    for row1 in rows6:
        row_num3 += 1
        for col_num5 in range(len(row1)):
            ws4.write(row_num3, col_num5, row1[col_num5], font_style)                

    #Hoja Preguntas
    
    for col_num6 in range(len(columnsws5)):
        ws5.write(row_num4, col_num6, columnsws5[col_num6], font_style)        

    font_style = xlwt.XFStyle()
    rows7 = Pregunta.objects.all().values_list('id_pregunta','pregunta', 'id_competencia', 'id_tipoCuest')

    for row1 in rows7:
        row_num4 += 1
        for col_num6 in range(len(row1)):
            ws5.write(row_num4, col_num6, row1[col_num6], font_style)

    #Hoja UTPL
        #Dependencia
    for col_num7 in range(len(columnsws8)):
        ws6.write(row_num5, col_num7, columnsws8[col_num7], font_style)        

    font_style = xlwt.XFStyle()
    rows8 = Dependencia.objects.all().values_list('id_dependencia','nombDependencia', 'id_area', 'id_tipoDep')

    for row1 in rows8:
        row_num5 += 1
        for col_num7 in range(len(row1)):
            ws6.write(row_num5, col_num7, row1[col_num7], font_style)

        #Facultades
    for col_num8 in range(len(columnsws9)):
        ws6.write(row_num5, col_num8, columnsws9[col_num8], font_style)        

    font_style = xlwt.XFStyle()
    rows9 = Area.objects.all().values_list('id_area','nombArea')

    for row1 in rows9:
        row_num5 += 1
        for col_num8 in range(len(row1)):
            ws6.write(row_num5, col_num8, row1[col_num8], font_style)        

    #DigComp
        #Competencias
    for col_num9 in range(len(columnsws10)):
        ws7.write(row_num6, col_num9, columnsws10[col_num9], font_style)        

    font_style = xlwt.XFStyle()
    rows10 = Competencia.objects.all().values_list('id_competencia','nombCompetencia', 'id_area_competencia')

    for row1 in rows10:
        row_num6 += 1
        for col_num9 in range(len(row1)):
            ws7.write(row_num6, col_num9, row1[col_num9], font_style)

        #Areas competencias
    for col_num10 in range(len(columnsws11)):
        ws7.write(row_num6, col_num10, columnsws11[col_num10], font_style)        

    font_style = xlwt.XFStyle()
    rows11 = Area_Competencia.objects.all().values_list('id_area_competencia','nombAreaCompetencia')

    for row1 in rows11:
        row_num6 += 1
        for col_num10 in range(len(row1)):
            ws7.write(row_num6, col_num10, row1[col_num10], font_style)   

    #Niveles recomendados
    for col_num11 in range(len(columnsws12)):
        ws8.write(row_num7, col_num11, columnsws12[col_num11], font_style)        

    font_style = xlwt.XFStyle()
    rows12 = Nivel.objects.all().values_list('id_nivel','nivel', 'id_competencia', 'id_dependencia')

    for row1 in rows12:
        row_num7 += 1
        for col_num11 in range(len(row1)):
            ws8.write(row_num7, col_num11, row1[col_num11], font_style)             

    #Respuestas cuestionario general
    for col_num12 in range(len(columnsws13)):
        ws9.write(row_num8, col_num12, columnsws13[col_num12], font_style)        

    font_style = xlwt.XFStyle()
    rows13 = RespuestaCuestionarioGeneral.objects.all().values_list('id','respuesta', 'valorRta', 'pregunta')

    for row1 in rows13:
        row_num8 += 1
        for col_num12 in range(len(row1)):
            ws9.write(row_num8, col_num12, row1[col_num12], font_style)   

    wb.save(response)
    return response    